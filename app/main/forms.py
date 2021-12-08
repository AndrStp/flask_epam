from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField,\
                    ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models.course import Course


class CourseForm(FlaskForm):
    """Form for creating courses"""
    label = StringField('Course name', validators=[DataRequired(), 
                                                   Length(3, 64)])
    small_desc = TextAreaField('Course description', validators=[DataRequired(),
                                                                 Length(3, 250)])
    exam = BooleanField('Exam')
    level = SelectField('Difficulty level', choices=[('I','Introductory'),
                                                     ('R', 'Regular'),
                                                     ('A', 'Advanced')])
    submit = SubmitField('Create')

    def validate_label(self, field):
        """Unique course name validation"""
        if Course.query.filter_by(label=field.data).first():
            raise ValidationError('Course name is already in use')

