from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)          # __name__ is a Python predefined variable that is
                               # set to name of the module in which it is used

app.config.from_object(Config) # sets the configuration details to be retrieved
                               # from the Config class in module config.py

miniblog_db = SQLAlchemy(app)
migrate = Migrate(app,miniblog_db)

from blog_app import routes, models # models module will define the structure of
                                    # of the database
