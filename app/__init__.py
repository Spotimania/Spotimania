
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#Set up of Flask App
app = Flask(__name__)
app.config.from_object(Config)

#Setup of Database
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

# Setup Session Logins
login = LoginManager(app)

#Getting All Routes and Database Models
from app import routes, models


