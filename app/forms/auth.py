from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models.users import User

class LoginForm(FlaskForm):
    login_id = StringField('Email or Username', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    role = SelectField('Account Type', choices=[('student', 'Student'), ('instructor', 'Instructor')], default='student')
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        from sqlalchemy import func
        clean_user = field.data.strip()
        if User.query.filter(func.lower(User.username) == clean_user.lower()).first():
            raise ValidationError('Username already taken. Please choose another username.')

    def validate_email(self, field):
        from sqlalchemy import func
        clean_email = field.data.strip().lower()
        if User.query.filter(func.lower(User.email) == clean_email).first():
            raise ValidationError('This email is already registered. Please sign in or reset your password.')

    def validate_password(self, field):
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Password must contain at least one digit.')


class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Optional(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=30)])
    country = StringField('Country', validators=[Optional(), Length(max=80)])
    bio = TextAreaField('About You / Bio', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')

    def validate_new_password(self, field):
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Password must contain at least one digit.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Reset Password')

    def validate_new_password(self, field):
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Password must contain at least one digit.')
