from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)          # __name__ is a Python predefined variable that is
                               # set to name of the module in which it is used

app.config.from_object(Config) # sets the configuration details to be retrieved
                               # from the Config class in module config.py

login = LoginManager(app)      # manages the user logged-in state
login.login_view = 'login'     # function name for login view

miniblog_db = SQLAlchemy(app)
migrate = Migrate(app,miniblog_db)

bootstrap = Bootstrap(app)

from blog_app import routes, models # models module will define the structure of
                                    # of the database
