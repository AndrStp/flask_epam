from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField,\
    ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    username = StringField('Username', 
                           validators=[DataRequired(),
                                       Length(3, 64),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 
                                              0,
                                              'Only letters, numbers, dots or '
                                              'underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password',
                                                             message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate(field):
        """Not registered email validation"""
        if User.query.get(email=field.data).first():
            raise ValidationError('Email\'s already in use')

    def validate_username(field: str):
        """Not used username validation"""
        if User.query.get(username=field.data).first():
            raise ValidationError('Username\'s already in use')
