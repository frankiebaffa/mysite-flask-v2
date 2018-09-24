# import flask forms from flask_wtf so forms
#   can be called to template from view
from flask_wtf import FlaskForm
# get fields for forms from wtforms
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, IntegerField
# get validator 'DataRequired' so that form fields can
#  require that they not be empty
from wtforms.validators import DataRequired

# login form with username, password, submit
class LoginForm(FlaskForm):
    # username string field
    username = StringField('Username', validators=[DataRequired()])
    # password password field
    password = PasswordField('Password', validators=[DataRequired()])
    # submit submit field
    submit = SubmitField('Sign In')

# contact form with name, email, subject, body, submit
class ContactForm(FlaskForm):
    # name string field
    name = StringField('Name', validators=[DataRequired()])
    # email string field
    email = StringField('Email Address', validators=[DataRequired()])
    # subject string field
    subject = StringField('Subject', validators=[DataRequired()])
    # bdoy text area field
    body = TextAreaField('Message', validators=[DataRequired()])
    # submit submit field
    submit = SubmitField('Send')

# content managing form with title, body, url, repo, submit
class ContentForm(FlaskForm):
    # title string field
    title = StringField('Title', validators=[DataRequired()])
    # body text area field
    body = TextAreaField('Enter your body in Markdown', validators=[DataRequired()])
    # url string field
    url = StringField('Content URL', validators=[DataRequired()])
    # repo string field
    repo = StringField('Repository URL', validators=[DataRequired()])
    # submit submit field
    submit = SubmitField('Submit')

class MusicForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    album = StringField('Album', validators=[DataRequired()])
    song0 = StringField('Song', validators=[DataRequired()])
    trackno0 = IntegerField('Track Number', validators=[DataRequired()])
    sc_api0 = IntegerField('SoundCloud API #', validators=[DataRequired()])
    descript0 = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
