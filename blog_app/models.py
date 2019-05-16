from blog_app import miniblog_db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from blog_app import login
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    username = miniblog_db.Column(miniblog_db.String(64), index = True, unique = True)
    email = miniblog_db.Column(miniblog_db.String(128), index = True, unique = True)
    password_hash = miniblog_db.Column(miniblog_db.String(128))
    posts = miniblog_db.relationship('Post', backref='author', lazy='dynamic')
    about_me = miniblog_db.Column(miniblog_db.String(140))
    last_seen = miniblog_db.Column(miniblog_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=retro&s={}".format(digest,size)

class Post(miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    body = miniblog_db.Column(miniblog_db.String(140))
    timestamp = miniblog_db.Column(miniblog_db.DateTime, index = True, default = datetime.utcnow)
    # Note in the default parameter we pass the function itself, and not the return value. Not utcnow(), just utcnow.
    user_id = miniblog_db.Column(miniblog_db.Integer, miniblog_db.ForeignKey('user.id'))
    # ForeignKey uses the database table name, and not the model class name unlike db.relationship

    def __repr__(self):
        return "<Post {}>".format(self.body)
