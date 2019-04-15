from blog_app import app, miniblog_db
from blog_app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {"miniblog_db":miniblog_db, "User":User, "Post":Post}
    
