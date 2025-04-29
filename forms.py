from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, RadioField, FileField


class UserForm(FlaskForm):

    username = StringField("Username")
    surname = StringField("Surname")
    age = IntegerField("Age")
    gender = SelectField("Gender", choices=[('erkek', 'e'), ('kadın', 'k')])
    file = FileField("File")
    submit = SubmitField('SEND')

    