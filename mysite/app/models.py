# get login from app to allow loading of users
from app import login
# import datetime for timestamps
from datetime import datetime
# import werkzeug.security generate_password_hash
#   for hashing and salting passwords
from werkzeug.security import generate_password_hash
# import werkzeug.security check_password_hash for login
from werkzeug.security import check_password_hash
# import db
from app import db
# get flask_login's mixin UserMixin
from flask_login import UserMixin

# Create a database model for users and include UserMixin
class User(UserMixin, db.Model):
    # Column id, type integer, primary key
    id = db.Column(db.Integer, primary_key=True)
    # Column username, type string, unique
    username = db.Column(db.String(64), index=True, unique=True)
    # Column email, type string, unique
    email = db.Column(db.String(120), index=True, unique=True)
    # Column password_hash, type string, salted hash of the user's password
    password_hash = db.Column(db.String(128))

    # When called, db object will print as 'User username'
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Method to set db stored password as a salted hash of user's
    #   preferred passwrd
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check user's password against the salted hash stored
    #   within the db
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# register user loader and pass user id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Create a database model for blog posts
class Blog(db.Model):
    # Column id, type integer, primary key
    id = db.Column(db.Integer, primary_key=True)
    # Column title, type string, 100 characters
    title = db.Column(db.String(100))
    # Column body, type string, 1000 characters
    body = db.Column(db.String(1000))
    # Column timestamp, type datetime, default now
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Column user_id, type integer, foreign key from User.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # When called, db object will print as 'Blog title'
    def __repr__(self):
        return '<Blog {}>'.format(self.title)

# Create a database model for projects
class Project(db.Model):
    # Column id, type integer, primary key
    id = db.Column(db.Integer, primary_key=True)
    # Column title, type string(100)
    title = db.Column(db.String(100))
    # Column body, type string (1000)
    body = db.Column(db.String(1000))
    # Column url, type string(100)
    url = db.Column(db.String(100))
    # Column repo, type string(100)
    repo = db.Column(db.String(100))
    # Column timestamp, type datetime
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Column user_id, type integer, foreign key from User.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # When called...
    def __repr__(self):
        return '<Project {}>'.format(self.title)

class Review(db.Model):
    # Column id, type integer, primary key
    id = db.Column(db.Integer, primary_key=True)
    # Column title, type string(100)
    title = db.Column(db.String(100))
    # Column body, type string (1000)
    body = db.Column(db.String(10000))
    # Column url, type string(100)
    url = db.Column(db.String(100))
    # Column timestamp, type datetime
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Column user_id, type integer, foreign key from User.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # When called...
    def __repr__(self):
        return '<Review {}>'.format(self.title)
