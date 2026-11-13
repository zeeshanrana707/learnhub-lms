from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ApplyCouponForm(FlaskForm):
    coupon_code = StringField('Promo / Discount Code', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Apply')


class CheckoutForm(FlaskForm):
    full_name = StringField('Cardholder / Billing Name', validators=[DataRequired(), Length(min=3, max=100)])
    payment_method = SelectField('Payment Method', choices=[
        ('simulated_card', 'Credit / Debit Card (Simulated Sandbox)'),
        ('simulated_bank', 'Direct Bank Transfer (Simulated)'),
        ('simulated_wallet', 'Digital Wallet (Simulated)')
    ], default='simulated_card')
    card_number = StringField('Card Number (Simulated - enter any 16 digits)', default='4242 4242 4242 4242', validators=[DataRequired()])
    card_expiry = StringField('Expiry Date', default='12/28', validators=[DataRequired()])
    card_cvc = StringField('Security Code (CVC)', default='123', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Complete Purchase & Enroll')
