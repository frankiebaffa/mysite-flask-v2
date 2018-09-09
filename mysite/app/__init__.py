# flask modules
from flask import Flask
# get configuration from Config
from config import Config
# SQLAlchemy for handling database
from flask_sqlalchemy import SQLAlchemy
# Migrate to handle db migrations
from flask_migrate import Migrate
# Use flask-login to manage user logged-in state
from flask_login import LoginManager

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

# get routes for application
from app import routes, models
