from flask import Flask, render_template, request
from config import Config
from flask_login import LoginManager #for logging users in and maintaining a session
from flask_sqlalchemy import SQLAlchemy #this talk to our database for us
from flask_migrate import Migrate #Makes altering the Database a lot easier


app = Flask(__name__)
app.config.from_object(Config)

# init Login Manager
login = LoginManager(app)
#where to be sent if you are not logged in
#there are settings in LoginManager. \
# login_view is one.
login.login_view = 'login'
# init the database from_object
db = SQLAlchemy(app)
# init Migrate. tells the app how to make changes\
#  to db without breaking anything
migrate = Migrate(app,db)

from app import routes