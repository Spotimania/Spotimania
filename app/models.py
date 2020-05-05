from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Define a base model for other database tables to inherit
# Useful for logging purposes
class Base(db.Model):

    __abstract__  = True

    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class BaseAutoPrimary(Base):
    __abstract__ = True
    id            = db.Column(db.Integer, primary_key=True)

# Login User Loader / Session Retriever
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Define a User model
class User(UserMixin,BaseAutoPrimary):

    __tablename__ = 'user'

    # User Name
    username    = db.Column(db.String(128), index=True, unique=True)

    # Identification Data: email & password
    email    = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    # Null Role refers to normal user
    privilegeId = db.Column(db.Integer, db.ForeignKey("privileges.id"))


    #Password Methods
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # New instance instantiation procedure
    def __init__(self, username, email, password,role=None):

        self.username     = username
        self.email    = email
        self.password_hash = generate_password_hash(password)
        self.role=role

    def __repr__(self):
        return '<User %r>' % (self.username)

class Privileges(BaseAutoPrimary):
    __tablename__ = "privileges"

    #privilege name
    name =db.Column(db.String(128), index=True, unique=True)

    # One To Many Relationship
    user = db.relationship("User",backref="role",lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Privileges %r>' % (self.name)

# Playlist model with track data
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    songID = db.Column(db.String(100))
    prevURL = db.Column(db.String(100))
    prevIMG = db.Column(db.String(100))
    songName = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))

