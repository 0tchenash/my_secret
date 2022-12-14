from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField, TextAreaField

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError, validators
from dao.models.models import User


class login_form(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[Optional()]
    )


class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )

    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("password", message="Passwords must match !"),
        ]
    )

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")

class contact_form(FlaskForm):
    username = StringField(
        validators=[Optional()]
    )
    text = StringField(validators=[Optional()])

    captcha = StringField(validators=[Optional()])

    def validate_uname(self, username):
        if not User.query.filter_by(username=username.data).first():
            raise ValidationError("Username doesn't exist!")