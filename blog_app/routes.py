from blog_app import app, miniblog_db
from flask import Flask,render_template,flash,redirect,url_for, request
from blog_app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from blog_app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():

    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        miniblog_db.session.add(post)
        miniblog_db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for('index'))

    posts = current_user.followed_posts().all()
    return render_template('index.html', title='Home', form=form, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm() # LoginForm imported at the top

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember = form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

        # flash('Login requested for user {}, remember_me={}'.format(
        # form.username.data, form.remember_me.data))
        # return redirect(url_for('index'))

    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        miniblog_db.session.add(user)
        miniblog_db.session.commit()
        flash('Congratulations! You have successfully registered.')
        return redirect(url_for('login'))

    return render_template("register.html", title="Register", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template("user.html", user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        miniblog_db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit profile", form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        miniblog_db.session.commit()    #didn't need to db.add since using current_user

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} does not exit".format(username))
        return redirect(url_for('index'))
    if user==current_user:
        flash("You can follow yourself")
        return redirect(url_for('user',username=username))
    current_user.follow(user)
    miniblog_db.session.commit()
    flash("You are now following {}".format(username))
    return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} does not exist".format(username))
        return redirect(url_for('index'))
    if user==current_user:
        flash("You can't unfollow yourself")
        return redirect(url_for('user',username=username))
    current_user.unfollow(user)
    miniblog_db.session.commit()
    flash("You have now unfollowed {}".format(username))
    return redirect(url_for('user',username=username))
