from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class UserForm (FlaskForm):
    profile_pic = FileField('Profile Picture')
