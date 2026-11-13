from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SelectMultipleField, BooleanField, DateTimeLocalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class UserAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()])
    is_active = BooleanField('Active Account')
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional(), Length(min=8)])
    submit = SubmitField('Save User')


class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=255)])
    permission_ids = SelectMultipleField('Assigned Permissions', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Role')


class CouponForm(FlaskForm):
    code = StringField('Coupon Code (uppercase alphanumeric)', validators=[DataRequired(), Length(min=2, max=50)])
    discount_percent = IntegerField('Discount Percentage (%)', default=10, validators=[NumberRange(min=1, max=100)])
    valid_from = DateTimeLocalField('Valid From', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    valid_to = DateTimeLocalField('Valid Until', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    usage_limit = IntegerField('Maximum Total Redemptions', default=100, validators=[NumberRange(min=1)])
    submit = SubmitField('Save Coupon')


class BadgeForm(FlaskForm):
    name = StringField('Badge Name', validators=[DataRequired(), Length(min=2, max=80)])
    description = StringField('Description', validators=[DataRequired(), Length(max=255)])
    icon = StringField('Bootstrap Icon Class (e.g. bi-award, bi-star-fill)', default='bi-award', validators=[DataRequired()])
    rule_code = StringField('Trigger Rule Code', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Save Badge')


class SettingForm(FlaskForm):
    key = StringField('Configuration Key', validators=[DataRequired(), Length(max=100)])
    value = TextAreaField('Value', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save Setting')


class RoadmapForm(FlaskForm):
    title = StringField('Roadmap Title', validators=[DataRequired(), Length(min=3, max=150)])
    slug = StringField('URL Slug (optional, auto-generated if blank)', validators=[Optional(), Length(max=150)])
    badge = StringField('Badge Label', default='Career Roadmap', validators=[Optional(), Length(max=80)])
    icon = StringField('Bootstrap Icon (e.g. bi-cpu-fill, bi-code-slash)', default='bi-diagram-3-fill', validators=[Optional(), Length(max=80)])
    estimated_duration = StringField('Estimated Duration (e.g. 4 - 6 Months)', default='3 - 5 Months', validators=[Optional(), Length(max=80)])
    bg_gradient = StringField('CSS Gradient Background', default='linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%)', validators=[Optional(), Length(max=255)])
    tagline = TextAreaField('Tagline / Quick Summary', validators=[Optional(), Length(max=255)])
    description = TextAreaField('Detailed Description', validators=[Optional()])
    skills_csv = TextAreaField('Key Skills (comma-separated, e.g. Python, Docker, PyTorch)', validators=[Optional()])
    target_roles_csv = TextAreaField('Target Job Roles (comma-separated, e.g. AI Engineer, Data Scientist)', validators=[Optional()])
    submit = SubmitField('Save Roadmap')


class RoadmapStageForm(FlaskForm):
    course_id = SelectField('Select Course to Add', coerce=int, validators=[DataRequired()])
    stage_label = StringField('Custom Stage Label (optional, e.g. Foundations)', validators=[Optional(), Length(max=80)])
    submit = SubmitField('Add Course as Stage')
