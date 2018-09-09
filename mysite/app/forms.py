# import flask forms from flask_wtf so forms
#   can be called to template from view
from flask_wtf import FlaskForm
# get fields for forms from wtforms
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField
# get validator 'DataRequired' so that form fields can
#  require that they not be empty
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
