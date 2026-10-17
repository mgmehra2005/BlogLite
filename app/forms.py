from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

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


class NewBlog(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Tittle is required')])
    blog = TextAreaField('Body', validators=[DataRequired(message="Body cann't be empty")])
    publish = SubmitField('Publish')


class Comment(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired(message='Comment cannot be empty'), Length(max=100, min=1)])
    post = SubmitField('Post')