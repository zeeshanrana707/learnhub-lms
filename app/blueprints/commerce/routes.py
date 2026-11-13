from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app.models.catalog import Course
from app.models.commerce import Order, Coupon
from app.forms.commerce import ApplyCouponForm, CheckoutForm
from app.services.orders import calculate_cart_breakdown, process_checkout
from app.utils.helpers import log_action

commerce_bp = Blueprint('commerce', __name__, url_prefix='/shop')

def get_cart_ids() -> list:
    return session.get('cart', [])


@commerce_bp.route('/cart')
def cart():
    """Shopping cart view."""
    cart_ids = get_cart_ids()
    coupon_code = session.get('coupon_code')
    courses, subtotal, discount, total, coupon, error_msg = calculate_cart_breakdown(cart_ids, coupon_code)

    if error_msg and coupon_code:
        flash(error_msg, 'warning')
        session.pop('coupon_code', None)

    coupon_form = ApplyCouponForm()
    return render_template(
        'commerce/cart.html',
        courses=courses,
        subtotal=subtotal,
        discount=discount,
        total=total,
        coupon=coupon,
        coupon_form=coupon_form
    )


@commerce_bp.route('/cart/add/<int:course_id>', methods=['POST'])
def add_to_cart(course_id):
    """Add course to session cart."""
    course = Course.query.get_or_404(course_id)
    cart = session.get('cart', [])
    if course.id not in cart:
        cart.append(course.id)
        session['cart'] = cart
        flash(f"'{course.title}' added to your shopping cart.", 'success')
    else:
        flash('Course is already in your cart.', 'info')

    return redirect(request.referrer or url_for('commerce.cart'))


@commerce_bp.route('/cart/remove/<int:course_id>', methods=['POST'])
def remove_from_cart(course_id):
    """Remove course from session cart."""
    cart = session.get('cart', [])
    if course_id in cart:
        cart.remove(course_id)
        session['cart'] = cart
        flash('Item removed from cart.', 'info')
    return redirect(url_for('commerce.cart'))


@commerce_bp.route('/cart/apply-coupon', methods=['POST'])
def apply_coupon():
    """Apply discount code."""
    form = ApplyCouponForm()
    if form.validate_on_submit():
        code = form.coupon_code.data.strip().upper()
        coupon = Coupon.query.filter_by(code=code).first()
        if not coupon:
            flash('Invalid coupon code.', 'danger')
        elif not coupon.is_valid():
            flash('Coupon has expired or usage limit exceeded.', 'danger')
        else:
            session['coupon_code'] = coupon.code
            flash(f"Coupon '{coupon.code}' applied ({coupon.discount_percent}% off)! 🎉", 'success')

    return redirect(url_for('commerce.cart'))


@commerce_bp.route('/cart/remove-coupon', methods=['POST'])
def remove_coupon():
    session.pop('coupon_code', None)
    flash('Coupon removed.', 'info')
    return redirect(url_for('commerce.cart'))


@commerce_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout and simulated payment."""
    cart_ids = get_cart_ids()
    if not cart_ids:
        flash('Your cart is empty. Please add courses first.', 'warning')
        return redirect(url_for('catalog.index'))

    coupon_code = session.get('coupon_code')
    courses, subtotal, discount, total, coupon, error = calculate_cart_breakdown(cart_ids, coupon_code)

    form = CheckoutForm()
    if request.method == 'GET' and current_user.profile:
        form.full_name.data = current_user.profile.full_name or current_user.username

    if form.validate_on_submit():
        # Process checkout and simulated transaction
        order, err = process_checkout(
            user=current_user,
            course_ids=cart_ids,
            coupon_code=coupon_code,
            payment_method=form.payment_method.data
        )

        if err:
            flash(f"Payment failed: {err}", 'danger')
            return redirect(url_for('commerce.checkout'))

        # Clear cart and applied coupon
        session.pop('cart', None)
        session.pop('coupon_code', None)

        flash(f"Payment of ${order.total:.2f} successful! You are now enrolled in your new courses.", 'success')
        return redirect(url_for('commerce.order_receipt', order_id=order.id))

    return render_template(
        'commerce/checkout.html',
        form=form,
        courses=courses,
        subtotal=subtotal,
        discount=discount,
        total=total,
        coupon=coupon
    )


@commerce_bp.route('/orders')
@login_required
def orders():
    """Student order history."""
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('commerce/orders.html', orders=user_orders)


@commerce_bp.route('/order/<int:order_id>')
@login_required
def order_receipt(order_id):
    """Detailed receipt view for an order."""
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to order receipt.', 'danger')
        return redirect(url_for('catalog.index'))

    return render_template('commerce/order_receipt.html', order=order)
