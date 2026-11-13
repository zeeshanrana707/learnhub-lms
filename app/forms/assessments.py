from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, BooleanField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired(), Length(min=3, max=150)])
    module_id = SelectField('Associated Module (Optional)', coerce=int, validators=[Optional()])
    time_limit_min = IntegerField('Time Limit (Minutes)', default=15, validators=[NumberRange(min=1, max=180)])
    max_attempts = IntegerField('Maximum Attempts Allowed', default=3, validators=[NumberRange(min=1, max=10)])
    pass_mark = DecimalField('Passing Percentage (%)', default=70.0, places=1, validators=[NumberRange(min=1, max=100)])
    submit = SubmitField('Save Quiz')


class QuestionForm(FlaskForm):
    text = TextAreaField('Question Prompt', validators=[DataRequired(), Length(min=5)])
    question_type = SelectField('Question Type', choices=[
        ('single_choice', 'Multiple Choice (Single Answer)'),
        ('true_false', 'True / False')
    ], default='single_choice')
    points = DecimalField('Points', default=1.0, places=1, validators=[NumberRange(min=0.5, max=100)])
    position = IntegerField('Position', default=1, validators=[NumberRange(min=1)])
    submit = SubmitField('Save Question')


class QuestionOptionForm(FlaskForm):
    text = StringField('Option Text', validators=[DataRequired(), Length(max=255)])
    is_correct = BooleanField('Mark as Correct Answer')
    submit = SubmitField('Add Option')


class RubricForm(FlaskForm):
    title = StringField('Rubric Name', validators=[DataRequired(), Length(min=3, max=150)])
    submit = SubmitField('Save Rubric')


class RubricCriterionForm(FlaskForm):
    description = StringField('Criterion Description', validators=[DataRequired(), Length(min=3, max=255)])
    max_points = DecimalField('Max Points', default=10.0, places=1, validators=[NumberRange(min=1)])
    submit = SubmitField('Add Criterion')


class AssignmentForm(FlaskForm):
    title = StringField('Assignment Title', validators=[DataRequired(), Length(min=3, max=150)])
    instructions = TextAreaField('Detailed Instructions', validators=[DataRequired(), Length(min=10)])
    due_date = DateTimeLocalField('Due Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    max_points = DecimalField('Maximum Points', default=100.0, places=1, validators=[NumberRange(min=1)])
    rubric_id = SelectField('Evaluation Rubric (Optional)', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Assignment')


class SubmissionForm(FlaskForm):
    text = TextAreaField('Your Answer / Work / Comments', validators=[Optional()])
    file = FileField('Attach File (PDF, ZIP, Code, Doc - max 16MB)', validators=[
        Optional(),
        FileAllowed(['pdf', 'zip', 'doc', 'docx', 'py', 'txt', 'png', 'jpg'], 'Unsupported file type!')
    ])
    submit = SubmitField('Submit Assignment')


class GradeForm(FlaskForm):
    score = DecimalField('Score / Points', places=1, validators=[NumberRange(min=0)])
    feedback = TextAreaField('Instructor Feedback', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Save Grade')
