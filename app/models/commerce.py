from datetime import datetime, timezone
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class Coupon(db.Model):
    __tablename__ = 'coupons'
    __table_args__ = (
        db.CheckConstraint('discount_percent >= 1 AND discount_percent <= 100', name='check_coupon_discount_range'),
    )

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    discount_percent = db.Column(db.Integer, nullable=False)
    valid_from = db.Column(db.DateTime, default=utcnow, nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, default=100, nullable=False)
    times_used = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    orders = db.relationship('Order', back_populates='coupon', lazy='select')

    def is_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        # handle naive or aware datetimes
        v_from = self.valid_from if self.valid_from.tzinfo else self.valid_from.replace(tzinfo=timezone.utc)
        v_to = self.valid_to if self.valid_to.tzinfo else self.valid_to.replace(tzinfo=timezone.utc)
        if now < v_from or now > v_to:
            return False
        if self.times_used >= self.usage_limit:
            return False
        return True

    def __repr__(self):
        return f'<Coupon {self.code} - {self.discount_percent}%>'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id', ondelete='SET NULL'), nullable=True)
    subtotal = db.Column(db.Float, default=0.0, nullable=False)
    discount = db.Column(db.Float, default=0.0, nullable=False)
    total = db.Column(db.Float, default=0.0, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, paid, failed
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship('User', back_populates='orders')
    coupon = db.relationship('Coupon', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan', lazy='selectin')
    payment = db.relationship('Payment', back_populates='order', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order #{self.id} User:{self.user_id} Total:${self.total} Status:{self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    price_at_purchase = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    order = db.relationship('Order', back_populates='items')
    course = db.relationship('Course', back_populates='order_items')

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Course:{self.course_id} Price:{self.price_at_purchase}>'


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    method = db.Column(db.String(50), default='simulated_card', nullable=False)  # card, simulated_card, paypal
    transaction_ref = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='completed', nullable=False)  # completed, failed
    paid_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    order = db.relationship('Order', back_populates='payment')

    def __repr__(self):
        return f'<Payment Ref:{self.transaction_ref} Amount:{self.amount} Status:{self.status}>'
