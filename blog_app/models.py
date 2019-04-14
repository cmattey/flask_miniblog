from blog_app import miniblog_db

class User(miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    username = miniblog_db.Column(miniblog_db.String(64), index = True, unique = True)
    email = miniblog_db.Column(miniblog_db.String(128), index = True, unique = True)
    password_hash = miniblog_db.Column(miniblog_db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)
        
