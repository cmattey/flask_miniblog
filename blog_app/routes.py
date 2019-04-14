from blog_app import app
from flask import Flask,render_template,flash,redirect,url_for
from blog_app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user,posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm() # LoginForm imported at the top

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
        form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('login.html', title = 'Sign In', form = form)