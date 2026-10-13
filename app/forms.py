from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required")])
    email = StringField('Email', validators=[DataRequired(message="Email is required"), Email(message='Invalid email address')])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="Please confirm your password"), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    submit = SubmitField('Login')


