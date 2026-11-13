from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from app.models.catalog import Course

class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[
        DataRequired(),
        Length(min=5, max=120, message='Course title must be between 5 and 120 characters.')
    ])
    slug = StringField('URL Slug', validators=[Optional(), Length(max=150)])
    description = TextAreaField('Course Description', validators=[
        DataRequired(),
        Length(min=20, message='Description must be at least 20 characters.')
    ])
    price = DecimalField('Price ($)', default=0.0, places=2, validators=[
        NumberRange(min=0, message='Course price cannot be negative.')
    ])
    level = SelectField('Skill Level', choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ], default='Beginner')
    status = SelectField('Publication Status', choices=[
        ('draft', 'Draft (Not visible in public catalog)'),
        ('published', 'Published (Live)'),
        ('archived', 'Archived')
    ], default='draft')
    department_id = SelectField('Department', coerce=int, validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    tag_ids = SelectMultipleField('Tags', coerce=int, validators=[Optional()])
    prerequisite_ids = SelectMultipleField('Prerequisites (Required Courses)', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Course')


class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Department')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    slug = StringField('Slug', validators=[Optional(), Length(max=120)])
    parent_id = SelectField('Parent Category (Optional)', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Category')


class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Save Tag')
