import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    #WTF FORM CONFIG
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_string"

    # SQL-ALCHEMY CONFIG
    # Fallback Option: Basedir/app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False