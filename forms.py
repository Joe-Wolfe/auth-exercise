from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class registerForm(FlaskForm):
    """form for registering a user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class loginForm(FlaskForm):
    """form for logging in a user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class feedbackForm(FlaskForm):
    """form for adding feedback"""

    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])
