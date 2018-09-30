# import application initialization
from app import app, db
# render_template for using Jinja2 templates
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask import Response
# get flask_login modules current_user and login_user
# also get flask_login module login_required to make sure
#   that login is validated before specific pages are accessed
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
# from models import User for login query
from app.models import User, Blog, Project, Review, Music, Typing, Access
from app.models import Access_Time
# get forms from app/forms.py
from app.forms import LoginForm, ContactForm, ContentForm, MusicForm
# get flask_mail for contact form
from flask_mail import Message, Mail
from sqlalchemy import func
import markdown2
import random
import re
import json
import urllib
# feedparser for handling .rss feeds
import feedparser

# create route 'index' at root of site and at '/index'
@app.route('/')
@app.route('/index')
# define function 'index'
def index():
    title = "Home"
    IPStore(title)
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
    IPStore(title)
    footer = ContentPostFooter()
    pagetype = "single"
    back = url_for('blog') + '#blog-container-' + str(post)
    return render_template("pages/blog.html", title=title, footer=footer,
            blog=blog, pagetype=pagetype, back=back)

@app.route('/blog')
def blog():
    title = "Blogs"
    IPStore(title)
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
    IPStore(title)
    footer = ContentPostFooter()
    back = url_for('projects') + '#project-container-' + str(post)
    return render_template("pages/projects.html", title=title, footer=footer,
            project=project, pagetype=pagetype, back=back)

@app.route('/projects')
def projects():
    title = "Projects"
    IPStore(title)
    footer = ContentFooter()
    projects = Project.query.order_by(Project.id.desc()).all()
    pagetype = "all"
    return render_template("pages/projects.html", title=title, footer=footer,
            projects=projects, pagetype=pagetype)

@app.route('/reviews')
def reviews():
    title = "Reviews"
    IPStore(title)
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
    IPStore(title)
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
    IPStore(title)
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
    IPStore(title)
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

#@app.route('/music/<artist>')
#def artist(artist):
#    title = "Music"
#    pagetype = "Artist"
#    songs = Music.query.filter(func.lower(func.replace(Music.artist, ' ', '')) == func.lower(func.replace(artist, '-', ''))).order_by(Music.trackno.asc()).all()
#    albumsarray = Music.query.distinct(Music.album).group_by(Music.album).filter(func.lower(func.replace(Music.artist, ' ', '')) == func.lower(func.replace(artist, '-', '')).order_by(Music.album.desc())).all()
#    albums = []
#    songarray = []
#    for album in albumsarray:
#        albums.append(album.album)
#    for i in range(len(albums)):
#        for song in songs:
#            album = []
#            if song.album == albums[i]:
#                album.append(song)
#        songarray.append(album)
#    header = (songs[0].artist).replace('-', ' ')
#    return render_template('pages/music.html', title=title, songs=songs, album.album, header=header, pagetype=pagetype)

@app.route('/music/<artist>/<album>')
def music(artist, album):
    title = "Music"
    IPStore(title)
    pagetype = "Album"
    songs = Music.query.filter(func.lower(func.replace(Music.artist, ' ', '')) == func.lower(func.replace(artist, '-', ''))).filter(func.lower(func.replace(Music.album, ' ', '')) == func.lower(func.replace(album, '-', ''))).order_by(Music.trackno.asc()).all()
    header = (songs[0].artist).replace('-', ' ')
    album = (songs[0].album).replace('-', ' ')
    return render_template('pages/music.html', title=title, songs=songs, header=header, album=album, pagetype=pagetype)

@app.route('/typing')
def typing():
    title = "Typing Test"
    IPStore(title)
    alltyping = Typing.query.all()
    integerarray = []
    for typing in alltyping:
        integerarray.append(typing.id)
    maxid = max(integerarray)
    randomint = random.randint(1, maxid)
    typing = Typing.query.filter(Typing.id == randomint).first()
    return render_template('pages/typing.html', title=title, typing=typing)

#=======================================#
#       All below methods must          #
#          @login_required              #
#=======================================#

# create route to manage method
# only allow if user is logged in
@app.route('/manage')
@login_required
def manage():
    title = "Manage"
    IPStore(title)
    footer = "These forms are used to create new objects within the SQLite3 database and to edit existing objects."
    projects = Project.query.all()
    blogs = Blog.query.all()
    reviews = Review.query.all()
    songs = Music.query.all()
    content = [projects, blogs, reviews, songs]
    users = User.query.all()
    form = ContentForm()
    musicform = MusicForm()
    return render_template('pages/manage.html', title=title, content=content,
            form=form, musicform=musicform, projects=projects, blogs=blogs, reviews=reviews,
            users=users, songs=songs, footer=footer)

mdown = markdown2.markdown

@app.route('/manage/createproject', methods=['POST'])
@login_required
def createproject():
    title = request.form.get("title")
    IPStore("Manage: "+title)
    body = request.form.get("body")
    body = mdown(body)
    body = body.replace("\n", "")
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
    IPStore("Manage: "+title)
    body = request.form.get("body")
    body = request.form.get("body")
    body = mdown(body)
    body = body.replace("\n", "")
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
    IPStore("Manage: "+title)
    body = request.form.get("body")
    body = mdown(body)
    body = body.replace("\n", "")
    blog = Blog(title=title, body=body, user_id=current_user.id)
    db.session.add(blog)
    db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/editblog', methods=['POST'])
@login_required
def editblog():
    blog_id = request.form.get("id")
    title = request.form.get("title")
    IPStore("Manage: "+title)
    body = request.form.get("body")
    body = mdown(body)
    body = body.replace("\n", "")
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
    IPStore("Manage: "+title)
    body = request.form.get("body")
    body = request.form.get("body")
    body = mdown(body)
    body = body.replace("\n", "")
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
    IPStore("Manage: "+title)
    body = request.form.get("body")
    body = request.form.get("body")
    body = mdown(body)
    body = body.replace("\n", "")
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

@app.route('/manage/createmusic', methods=['POST'])
@login_required
def createmusic():
    IPStore("Manage: Music Create Attempt")
    for i in range(int(request.form.get("song-add-counter")) + 1):
        artist = request.form.get("artist")
        album = request.form.get("album")
        song = request.form.get("song" + str(i))
        trackno = request.form.get("trackno" + str(i))
        sc_api = request.form.get("sc_api" + str(i))
        descript = request.form.get("descript" + str(i))
        descript = mdown(descript)
        descript = descript.replace("\n", "")
        music = Music(artist=artist, album=album, song=song,trackno=trackno,
                sc_api=sc_api, descript=descript)
        db.session.add(music)
        db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/editmusic', methods=['POST'])
@login_required
def editmusic():
    music_id = int(request.form.get("id"))
    artist = request.form.get("artist")
    album = request.form.get("album")
    song = request.form.get("song0")
    IPStore("Manage: "+song)
    trackno = request.form.get("trackno0")
    sc_api = request.form.get("sc_api0")
    descript = request.form.get("descript0")
    descript = mdown(descript)
    descript = descript.replace("\n", "")
    music = Music.query.filter(Music.id==music_id).first()
    music.artist = artist
    music.album = album
    music.song = song
    music.trackno = trackno
    music.sc_api = sc_api
    music.descript = descript
    db.session.add(music)
    db.session.commit()
    return redirect(url_for('manage'))

@app.route('/manage/logdl.txt', methods=['GET', 'POST'])
@login_required
def iplog():
    logs = db.session.query(Access.ip, Access.loc, Access_Time.timestamp,
            Access_Time.page).join(Access_Time).order_by(Access_Time.timestamp.desc()).all()
    def generate():
        for log in logs:
            for attrib in log:
                yield '{}\n'.format(attrib)
            yield '\n'
    return Response(generate(),
                    mimetype="text/plain",
                    headers={"Content-disposition":
                             "attachment;filename=iplog.txt"})
    

# create route to logout method
# only allow if user is logged in
@app.route('/logout')
@login_required
def logout():
    title = "Logout"
    IPStore(title)
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

def IPStore(title):
    url = 'http://ipinfo.io/json'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    ip = data['ip']
    org = data['org']
    city = data['city']
    country = data['country']
    region = data['region']
    a = Access.query.filter(Access.ip == ip).first()
    if not a:
        a = Access(ip=ip,
                   org=org,
                   loc="{}, {}, {}".format(city, region, country))
    db.session.add(a)
    db.session.commit()
    t = Access_Time(ip_id=a.id, page=title)
    db.session.add(t)
    db.session.commit()
