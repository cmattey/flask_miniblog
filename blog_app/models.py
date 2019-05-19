from blog_app import miniblog_db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from blog_app import login
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
Note that I am not declaring this table as a model, like I did for the users
and posts tables. Since this is an auxiliary table that has no data other than
the foreign keys, I created it without an associated model class.
"""
followers = miniblog_db.Table('followers',
            miniblog_db.Column('follower_id',miniblog_db.Integer,miniblog_db.ForeignKey('user.id')),
            miniblog_db.Column('followed_id',miniblog_db.Integer,miniblog_db.ForeignKey('user.id'))
            )

class User(UserMixin, miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    username = miniblog_db.Column(miniblog_db.String(64), index = True, unique = True)
    email = miniblog_db.Column(miniblog_db.String(128), index = True, unique = True)
    password_hash = miniblog_db.Column(miniblog_db.String(128))
    about_me = miniblog_db.Column(miniblog_db.String(140))
    last_seen = miniblog_db.Column(miniblog_db.DateTime, default=datetime.utcnow)

    posts = miniblog_db.relationship('Post', backref='author', lazy='dynamic')

    """
    This relationship links User instances to other User instances, so as a
    convention let's say that for a pair of users linked by this relationship,
    the left side user is following the right side user.
    secondary: configures the association table that is used for this
    relationship, which I defined right above this class.

    Parameter explanations->
    'User': is the right side entity of the relationship (the left side entity
    is the parent class). Since this is a self-referential relationship, I have
    to use the same class on both sides.

    secondary: configures the association table that is used for this
    relationship, which I defined right above this class.

    primaryjoin: indicates the condition that links the left side entity (the
    follower user) with the association table. The join condition for the left
    side of the relationship is the user ID matching the follower_id field of
    the association table. The followers.c.follower_id expression references
    the follower_id column of the association table.

    secondaryjoin: indicates the condition that links the right side entity (the
    followed user) with the association table. This condition is similar to the
    one for primaryjoin, with the only difference that now I'm using
    followed_id, which is the other foreign key in the association table.

    backref: defines how this relationship will be accessed from the right side
    entity. From the left side, the relationship is named followed, so from the
    right side I am going to use the name followers to represent all the left
    side users that are linked to the target user in the right side. The additional
    lazy argument indicates the execution mode for this query. A mode of dynamic
    sets up the query to not run until specifically requested, which is also how
    I set up the posts one-to-many relationship.

    lazy: is similar to the parameter of the same name in the backref, but this
    one applies to the left side query instead of the right side
    """
    followed = miniblog_db.relationship('User', secondary=followers,
                primaryjoin=(followers.c.follower_id == id),
                secondaryjoin=(followers.c.followed_id == id),
                backref=miniblog_db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=retro&s={}".format(digest,size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if not self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    """
    join():
    I'm invoking the join operation on the posts table. The first argument is
    the followers association table, and the second argument is the join
    condition. What I'm saying with this call is that I want the database to
    create a temporary table that combines data from posts and followers tables.
    The data is going to be merged according to the condition that I passed as
    argument.
    filter():
    The filter() call selects the items in the joined table that have the
    follower_id column set to this user, which in other words means that I'm
    keeping only the entries that have this user as a follower.

    Remember that the query was issued on the Post class, so even though I ended
    up with a temporary table that was created by the database as part of this
    query, the result will be the posts that are included in this temporary
    table, without the extra columns added by the join operation.
    """
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id ==  Post.user_id)).filter(
            followers.c.follower_id == self.id)
        # To get own posts along with followed posts
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(miniblog_db.Model):
    id = miniblog_db.Column(miniblog_db.Integer, primary_key = True)
    body = miniblog_db.Column(miniblog_db.String(140))
    timestamp = miniblog_db.Column(miniblog_db.DateTime, index = True, default = datetime.utcnow)
    # Note in the default parameter we pass the function itself, and not the return value. Not utcnow(), just utcnow.
    user_id = miniblog_db.Column(miniblog_db.Integer, miniblog_db.ForeignKey('user.id'))
    # ForeignKey uses the database table name, and not the model class name unlike db.relationship

    def __repr__(self):
        return "<Post {}>".format(self.body)
