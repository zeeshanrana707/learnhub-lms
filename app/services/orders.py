import uuid
from datetime import datetime, timezone
from app.extensions import db
from app.models.catalog import Course
from app.models.commerce import Order, OrderItem, Payment, Coupon
from app.models.content import Enrollment, Wishlist
from app.models.users import Notification, User
from app.utils.helpers import log_action

def calculate_cart_breakdown(course_ids: list, coupon_code: str = None):
    """
    Given a list of course IDs and optional coupon code,
    return (courses, subtotal, discount, total, coupon_obj, error_msg).
    """
    if not course_ids:
        return [], 0.0, 0.0, 0.0, None, "Cart is empty."

    courses = Course.query.filter(Course.id.in_(course_ids), Course.is_active == True).all()
    subtotal = sum(c.price for c in courses)

    coupon = None
    discount = 0.0
    error_msg = None

    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code.strip().upper()).first()
        if not coupon:
            error_msg = "Invalid coupon code."
        elif not coupon.is_valid():
            error_msg = "Coupon has expired or reached its maximum usage limit."
            coupon = None
        else:
            discount = round(subtotal * (coupon.discount_percent / 100.0), 2)

    total = round(max(0.0, subtotal - discount), 2)
    return courses, subtotal, discount, total, coupon, error_msg


def process_checkout(user: User, course_ids: list, coupon_code: str = None, payment_method: str = 'simulated_card') -> tuple[Order | None, str | None]:
    """
    Process order creation, payment simulation, and auto-enrollment.
    Returns (order, error_message).
    """
    courses, subtotal, discount, total, coupon, error_msg = calculate_cart_breakdown(course_ids, coupon_code)
    if not courses:
        return None, "No valid courses in cart."

    try:
        # 1. Create Order
        order = Order(
            user_id=user.id,
            coupon_id=coupon.id if coupon else None,
            subtotal=subtotal,
            discount=discount,
            total=total,
            status='paid',
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(order)
        db.session.flush()

        # 2. Create Order Items
        for course in courses:
            item = OrderItem(
                order_id=order.id,
                course_id=course.id,
                price_at_purchase=course.price
            )
            db.session.add(item)

        # 3. Increment coupon usage
        if coupon:
            coupon.times_used += 1

        # 4. Record simulated payment
        txn_ref = f"SIM-TXN-{uuid.uuid4().hex[:10].upper()}"
        payment = Payment(
            order_id=order.id,
            method=payment_method,
            transaction_ref=txn_ref,
            amount=total,
            status='completed',
            paid_at=datetime.now(timezone.utc)
        )
        db.session.add(payment)

        # 5. Automatically enroll the user in purchased courses
        for course in courses:
            existing_enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course.id).first()
            if not existing_enrollment:
                enrollment = Enrollment(
                    user_id=user.id,
                    course_id=course.id,
                    status='active',
                    progress_pct=0.0,
                    enrolled_at=datetime.now(timezone.utc)
                )
                db.session.add(enrollment)

            # Remove from wishlist if it was there
            Wishlist.query.filter_by(user_id=user.id, course_id=course.id).delete()

        # 6. Send notification
        notif = Notification(
            user_id=user.id,
            title="Order Confirmed! 🚀",
            message=f"Your order #{order.id} for ${total:.2f} was successful. Courses have been added to your My Learning page.",
            link=f"/shop/order/{order.id}"
        )
        db.session.add(notif)
        db.session.commit()

        log_action(user, 'checkout', 'Order', order.id, f"Order #{order.id} completed. Total: ${total:.2f}")
        return order, None

    except Exception as e:
        db.session.rollback()
        return None, str(e)
