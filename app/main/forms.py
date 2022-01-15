from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField,\
                    ValidationError, TextAreaField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, Optional
from app.models.course import Course


class CourseForm(FlaskForm):
    """Form for creating and editing a course"""
    label = StringField('Course label', validators=[DataRequired(),
                                                   Length(3, 64)])
    small_desc = TextAreaField('Course description', validators=[DataRequired(),
                                                                 Length(3, 250)])
    exam = BooleanField('Exam')
    level = SelectField('Difficulty level', choices=[('I', 'Introductory'),
                                                     ('R', 'Regular'),
                                                     ('A', 'Advanced')])
    submit = SubmitField('Create')

    def __init__(self, course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course

    def validate_label(self, field):
        """Unique course name validation"""
        if self.course:
            if field.data != self.course.label and \
                Course.query.filter_by(label=field.data).first():
                raise ValidationError('Course name is already in use')
        else:
            if Course.query.filter_by(label=field.data).first():
                raise ValidationError('Course name is already in use')


class CourseSearchForm(FlaskForm):
    """Form for searching"""
    username = StringField('Author name', validators=[Optional(), Length(3, 64)])
    start_date = DateField('Created From', validators=[Optional()])
    end_date = DateField('Created To', validators=[Optional()])
    exam = SelectField('Exam', choices=[('', 'All courses'),
                                        ('true', 'With exam'),
                                        ('false', 'No exam')])
    level = SelectField('Difficulty level', choices=[('', 'All levels'),
                                                     ('I', 'Introductory'),
                                                     ('R', 'Regular'),
                                                     ('A', 'Advanced')])
    submit = SubmitField('Search')
