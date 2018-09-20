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
from app.models import User, Blog, Project, Review
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
    title = "Home"
    footer = "FrankieBaffa.com was made using the Flask Micro-Framework for Python"
    projects = Project.query.order_by(Project.id.desc()).limit(5).all()
    blog = Blog.query.order_by(Blog.id.desc()).limit(5).all()
    reviews = Review.query.order_by(Review.id.desc()).limit(5).all()
    pagetype = "top"
    return render_template('pages/index.html', projects=projects, title=title,
            blog=blog, reviews=reviews, pagetype=pagetype, footer=footer)

@app.route('/blog/<post>', methods=['GET'])
def blogpost(post):
    blog = Blog.query.filter(Blog.id == post).first()
    title = blog.title
    footer = ContentPostFooter()
    pagetype = "single"
    back = url_for('blog') + '#blog-container-' + str(post)
    return render_template("pages/blog.html", title=title, footer=footer,
            blog=blog, pagetype=pagetype, back=back)

@app.route('/blog')
def blog():
    title = "Blogs"
    footer = ContentFooter()
    blog = Blog.query.order_by(Blog.id.desc()).all()
    pagetype = "all"
    return render_template("pages/blog.html", title=title, footer=footer,
            blog=blog, pagetype=pagetype)

@app.route('/projects/<post>', methods=['GET'])
def projectpost(post):
    pagetype = "single"
    project = Project.query.filter(Project.id == post).first()
    title = project.title
    footer = ContentPostFooter()
    back = url_for('projects') + '#project-container-' + str(post)
    return render_template("pages/projects.html", title=title, footer=footer,
            project=project, pagetype=pagetype, back=back)

@app.route('/projects')
def projects():
    title = "Projects"
    footer = ContentFooter()
    projects = Project.query.order_by(Project.id.desc()).all()
    pagetype = "all"
    return render_template("pages/projects.html", title=title, footer=footer,
            projects=projects, pagetype=pagetype)

@app.route('/reviews')
def reviews():
    title = "Reviews"
    footer = ContentFooter()
    reviews = Review.query.order_by(Review.id.desc()).all()
    pagetype = "all"
    return render_template("pages/reviews.html", title=title, footer=footer,
            reviews=reviews, pagetype=pagetype)

@app.route('/reviews/<post>', methods=['GET'])
def reviewpost(post):
    pagetype = "single"
    review = Review.query.filter(Review.id == post).first()
    title = review.title
    footer = ContentPostFooter()
    back = url_for('reviews') + '#review-container-' + str(post)
    return render_template("pages/reviews.html", title=title, footer=footer,
            review=review, pagetype=pagetype, back=back)


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
    title = "Login"
    footer = "This unlinked page is the login form, used to access the CMS."
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
    return render_template('pages/login.html', title=title, form=form,
            footer=footer)

# create route to contact method
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    title = "Contact"
    footer = "Forms are created using WTForms combined with Bootstrap 4 classes."
    mail = Mail()
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('pages/contact.html', title=title, footer=footer,
                    form=form)
        else:
            msg = Message(form.subject.data, sender=app.config['MAIL_USERNAME'],
                    recipients=[app.config['CONTACT_EMAIL']])
            msg.body = ContactEmail(form.name.data, form.email.data, form.body.data)
            mail.send(msg)
            confirm = Message('Contact Confirmation',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[form.email.data])
            confirm.body = ConfirmationEmail(form.name.data)
            mail.send(confirm)
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        return render_template('pages/contact.html', title=title, footer=footer,
                form=form)

#=======================================#
#       All below methods must          #
#          @login_required              #
#=======================================#

# create route to manage method
# only allow if user is logged in
@app.route('/manage')
@login_required
def manage():
    title = "Manage Content"
    footer = "These forms are used to create new objects within the SQLite3 database and to edit existing objects."
    projects = Project.query.all()
    blogs = Blog.query.all()
    reviews = Review.query.all()
    content = [projects, blogs, reviews]
    users = User.query.all()
    form = ContentForm()
    return render_template('pages/manage.html', title=title, content=content,
            form=form, projects=projects, blogs=blogs, reviews=reviews,
            users=users, footer=footer)

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

@app.route('/manage/createreview', methods=['POST'])
@login_required
def createreview():
    title = request.form.get("title")
    body = request.form.get("body")
    url = request.form.get("url")
    repo = request.form.get("repo")
    review = Review(title=title, body=body, url=url, repo=repo,
            user_id=current_user.id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/editreview', methods=['POST'])
@login_required
def editreview():
    review_id = request.form.get("id")
    title = request.form.get("title")
    body = request.form.get("body")
    url = request.form.get("url")
    repo = request.form.get("repo")
    review = Review.query.filter(Review.id==review_id).first()
    review.title = title
    review.body = body
    review.url = url
    review.repo = repo
    db.session.add(review)
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

def ContentFooter():
    footer = "Content pages are dynamically generated using a SQLite3 database queried by SQLAlchemy. (Also, notice the dynamic navbar)"
    return footer

def ContentPostFooter():
    footer = "Individual content post pages are passed into a dynamic route in view which fills the reusable template."
    return footer
