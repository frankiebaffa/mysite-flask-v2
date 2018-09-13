# import application initialization
from app import app, db
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
from app.forms import LoginForm, ContactForm, ContentForm
# get flask_mail for contact form
from flask_mail import Message, Mail
# feedparser for handling .rss feeds
import feedparser

# create route 'index' at root of site and at '/index'
@app.route('/')
@app.route('/index')
# define function 'index'
def index():
    projects = Project.query.order_by(Project.id.desc()).limit(5).all()
    blog = Blog.query.order_by(Blog.id.desc()).limit(5).all()
    pagetype = "top"
    # return template at 'pages/index.html'
    return render_template('pages/index.html', projects=projects, blog=blog, pagetype=pagetype)

@app.route('/blog/<post>', methods=['GET'])
def blogpost(post):
    blog = Blog.query.filter(Blog.id == post).first()
    pagetype = "single"
    back = url_for('blog') + '#blog-container-' + str(post)
    return render_template("pages/blogpost.html", blog=blog, pagetype=pagetype, back=back)

@app.route('/blog')
def blog():
    blog = Blog.query.all()
    pagetype = "all"
    return render_template("pages/blog.html", blog=blog, pagetype=pagetype)

@app.route('/project/<post>', methods=['GET'])
def projectpost(post):
    projectpost = Project.query.filter(Project.id == post).first()
    return render_template("pages/projectpost.html", projectpost=projectpost)


## create route 'news' at '/news'
#@app.route('/news')
## define function news
#def news():
#    # define variable feed as feedparser reddit.com/r/worldnews
#    feed = feedparser.parse('http://reddit.com/r/worldnews.rss')
#    # return template at 'pages/news.html' and 'feed'
#    return render_template('pages/news.html', feed=feed)

# create route to login page at '/login'
# if user is already authenticated, forward to '/manage'
# if form validate on submit, log user in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('manage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            message = 'Invalid username or password'
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('manage'))
    return render_template('pages/login.html', title='Sign In', form=form)

# create route to contact method
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    mail = Mail()
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('pages/contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['CONTACT_EMAIL']])
            msg.body = ContactEmail(form.name.data, form.email.data, form.body.data)
            mail.send(msg)
            confirm = Message('Contact Confirmation', sender=app.config['MAIL_USERNAME'],
                recipients=[form.email.data])
            confirm.body = ConfirmationEmail(form.name.data)
            mail.send(confirm)
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        return render_template('pages/contact.html', form=form)

#=======================================#
#       All below methods must          #
#          @login_required              #
#=======================================#

# create route to manage method
# only allow if user is logged in
@app.route('/manage')
@login_required
def manage():
    projects = Project.query.all()
    blogs = Blog.query.all()
    content = [projects, blogs]
    form = ContentForm()
    return render_template('pages/manage.html', content=content,
            form=form, projects=projects, blogs=blogs)

@app.route('/manage/createproject', methods=['POST'])
@login_required
def createproject():
    title = request.form.get("title")
    body = request.form.get("body")
    url = request.form.get("url")
    repo = request.form.get("repo")
    project = Project(title=title, body=body, url=url, repo=repo,
            user_id=current_user.id)
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/editproject', methods=['POST'])
@login_required
def editproject():
    project_id = request.form.get("id")
    title = request.form.get("title")
    body = request.form.get("body")
    url = request.form.get("url")
    repo = request.form.get("repo")
    project = Project.query.filter(Project.id==project_id).first()
    project.title = title
    project.body = body
    project.url = url
    project.repo = repo
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/createblog', methods=['POST'])
@login_required
def createblog():
    title = request.form.get("title")
    body = request.form.get("body")
    blog = Blog(title=title, body=body, user_id=current_user.id)
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/editblog', methods=['POST'])
@login_required
def editblog():
    blog_id = request.form.get("id")
    title = request.form.get("title")
    body = request.form.get("body")
    blog = Blog.query.filter(Blog.id==blog_id).first()
    blog.title = title
    blog.body = body
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for('manage'))

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

