# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm  # , RecaptchaField

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.controllers import *


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    rememberMe = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', [EqualTo('password')])
    email = StringField('Email', [Email(),DataRequired()])
    submit = SubmitField("Register Now")

    # Database Validation : WTFForm specification : def validate_<field Name>(self, <field name>)
    def validate_email(self, email):
        if (isEmailTaken(email.data)):
            raise ValidationError("Email Is Already In Use")

    def validate_username(self, username):
        if (isUsernameTaken(username.data)):
            raise ValidationError("Username Is Already In Use")

class RegisterAdminForm(RegisterForm):
    specialPassword = PasswordField("Special Password", [DataRequired()])
