from blog_app import miniblog_db
from datetime import datetime

class User(miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    username = miniblog_db.Column(miniblog_db.String(64), index = True, unique = True)
    email = miniblog_db.Column(miniblog_db.String(128), index = True, unique = True)
    password_hash = miniblog_db.Column(miniblog_db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

class Post(miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    body = miniblog_db.Column(miniblog_db.String(140))
    timestamp = miniblog_db.Column(miniblog_db.DateTime, index = True, default = datetime.utcnow)
    # Note in the default parameter we pass the function itself, and not the return value. Not utcnow(), just utcnow.
    user_id = miniblog_db.Column(miniblog_db.Integer, miniblog_db.ForeignKey('user.id'))
    # ForeignKey uses the database table name, and not the model class name unlike db.relationship

    def __repr__(self):
        return "<Post {}>".format(self.body)
