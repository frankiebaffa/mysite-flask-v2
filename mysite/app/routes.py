# import application initialization
from app import app
# render_template for using Jinja2 templates
from flask import render_template, flash, redirect, url_for, request
# get flask_login modules current_user and login_user
# also get flask_login module login_required to make sure
#   that login is validated before specific pages are accessed
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
# from models import User for login query
from app.models import User, Blog, Project
# get forms from app/forms.py
from app.forms import LoginForm, ContactForm
# get flask_mail for contact form
from flask_mail import Message, Mail
# feedparser for handling .rss feeds
import feedparser

# create route 'index' at root of site and at '/index'
@app.route('/')
@app.route('/index')
# define function 'index'
def index():
    projects = Project.query.limit(10).all()
    blogs = Blog.query.limit(10).all()
    # return template at 'pages/index.html'
    return render_template('pages/index.html', projects=projects, blogs=blogs)

@app.route('/blog/<post>', methods=['GET'])
def blogpost(post):
    blogpost = Blog.query.filter(Blog.id == post).first()
    return render_template("pages/blogpost.html", blogpost=blogpost)

@app.route('/project/<post>', methods=['GET'])
def projectpost(post):
    projectpost = Project.query.filter(Project.id == post).first()
    return render_template("pages/projectpost.html", projectpost=projectpost)


# create route 'news' at '/news'
@app.route('/news')
# define function news
def news():
    # define variable feed as feedparser reddit.com/r/worldnews
    feed = feedparser.parse('http://reddit.com/r/worldnews.rss')
    # return template at 'pages/news.html' and 'feed'
    return render_template('pages/news.html', feed=feed)

# create route to login page at '/login'
# if user is already authenticated, forward to '/manage'
# if form validate on submit, log user in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('pages/login.html', title='Sign In', form=form)

# create route to contact method
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    mail = Mail()
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            message = 'All fields are required.'
            return render_template('pages/contact.html', form=form, message=message)
        else:
            msg = Message(form.subject.data, sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['CONTACT_EMAIL']])
            msg.body = ContactEmail(form.name.data, form.email.data, form.body.data)
            mail.send(msg)
            confirm = Message('Contact Confirmation', sender=app.config['MAIL_USERNAME'],
                recipients=[form.email.data])
            confirm.body = ConfirmationEmail(form.name.data)
            mail.send(confirm)
            message = 'Your message has been sent!'
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        message = ''
        return render_template('pages/contact.html', form=form, message=message)


# create route to logout method
# only allow if user is logged in
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def ContactEmail(name, email, body):
    message = """
From: {} <{}>

{}
    """.format(name, email, body)
    return message

def ConfirmationEmail(name):
    message = """
Hello {},

This email is confirming that your contact request from frankiebaffa.com has been sent.

If you did not fill out the contact form on frankiebaffa.com/contact then please disregard this email.

I will attempt to get back to you as soon as possible!

 Frankie
    """.format(name)
    return message

