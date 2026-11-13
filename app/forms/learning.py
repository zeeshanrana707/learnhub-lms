from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ModuleForm(FlaskForm):
    title = StringField('Module Title', validators=[DataRequired(), Length(min=3, max=150)])
    position = IntegerField('Order / Position', default=1, validators=[NumberRange(min=1)])
    submit = SubmitField('Save Module')


class LessonForm(FlaskForm):
    title = StringField('Lesson Title', validators=[DataRequired(), Length(min=3, max=150)])
    content = TextAreaField('Lesson Content (Markdown / Text / Embed Code)', validators=[DataRequired()])
    content_type = SelectField('Content Type', choices=[
        ('text', 'Text / Markdown Article'),
        ('video_url', 'Video URL (YouTube/Vimeo/Embed)'),
        ('reading', 'Reading Material')
    ], default='text')
    duration_min = IntegerField('Estimated Duration (Minutes)', default=10, validators=[NumberRange(min=1)])
    position = IntegerField('Order / Position', default=1, validators=[NumberRange(min=1)])
    submit = SubmitField('Save Lesson')


class LessonResourceForm(FlaskForm):
    title = StringField('Resource Title', validators=[DataRequired(), Length(min=2, max=150)])
    resource_type = SelectField('Type', choices=[
        ('link', 'External Link / URL'),
        ('pdf', 'PDF Document Link'),
        ('code', 'Code Repository / Gist'),
        ('notes', 'Reference Notes')
    ], default='link')
    url_or_path = StringField('URL or File Location', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add Resource')


class AnnouncementForm(FlaskForm):
    title = StringField('Announcement Title', validators=[DataRequired(), Length(min=3, max=150)])
    body = TextAreaField('Message to Enrolled Students', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Post Announcement')


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        ('5', '⭐⭐⭐⭐⭐ (5/5 - Outstanding)'),
        ('4', '⭐⭐⭐⭐ (4/5 - Very Good)'),
        ('3', '⭐⭐⭐ (3/5 - Good)'),
        ('2', '⭐⭐ (2/5 - Fair)'),
        ('1', '⭐ (1/5 - Poor)')
    ], default='5', coerce=int)
    comment = TextAreaField('Your Review & Feedback', validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField('Submit Review')
