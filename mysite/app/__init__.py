# flask modules
from flask import Flask
# import babel
import babel
# get configuration from Config
from config import Config
from mail import MailConfig
# SQLAlchemy for handling database
from flask_sqlalchemy import SQLAlchemy
# Migrate to handle db migrations
from flask_migrate import Migrate
# Use flask-login to manage user logged-in state
from flask_login import LoginManager
# Import Mail from flask_mail
from flask_mail import Mail
from flaskext.markdown import Markdown
import re

# set application name as name
app = Flask(__name__)
# configure application from Config
app.config.from_object(Config)
# initialize SQLAlchemy
db = SQLAlchemy(app)
# initialize flask-migrate
migrate = Migrate(app, db)
# initialize login manager
login = LoginManager(app)
login.login_view = 'login'
# configure application from MailConfig
MailConfig(app)

mail = Mail()
mail.init_app(app)

Markdown(app)

# create a jinja filter for datetime using babel
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, MMM d, y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)

def format_hyphens(value):
    return value.replace('-', ' ')

def markup_strip(value):
    return re.sub(r'<.+?>', '', value)

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['hyphens'] = format_hyphens
app.jinja_env.filters['markstrip'] = markup_strip


# get routes for application
from app import routes, models
