from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ThreadForm(FlaskForm):
    title = StringField('Discussion Topic / Question', validators=[DataRequired(), Length(min=5, max=150)])
    body = TextAreaField('Details / Opening Post', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Start Discussion')


class PostForm(FlaskForm):
    body = TextAreaField('Your Reply', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Post Reply')


class MessageForm(FlaskForm):
    recipient_id = SelectField('Recipient', coerce=int, validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=150)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Send Message')
