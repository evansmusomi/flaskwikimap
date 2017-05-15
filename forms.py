""" Defines form backends """

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(Form):
    """ Defines the sign up form fields """

    first_name = StringField('First name',
                             validators=[DataRequired('Please enter your first name')])

    last_name = StringField('Last name',
                            validators=[DataRequired('Please enter your last name')])

    email = StringField('Email',
                        validators=[
                            DataRequired('Please enter your email'),
                            Email('Please enter your email')])

    password = PasswordField('Password',
                             validators=[
                                 DataRequired('Please enter your password'),
                                 Length(
                                     min=6,
                                     message='Password must be 6 or more characters')])
    submit = SubmitField('Sign up')
