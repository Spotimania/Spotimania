from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Checking Types
from sqlalchemy.orm.attributes import InstrumentedAttribute
import types

# Define a base model for other database tables to inherit
# Useful for logging purposes


class Base(db.Model):

    __abstract__ = True

    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def to_dict(self):
        classVars = vars(type(self))  # get any "default" attrs defined at the class level
        instanceVars = vars(self)  # get any attrs defined on the instance (self)
        allVars = dict(classVars)
        allVars.update(instanceVars)
        # filter out private attributes, functions and SQL_Alchemy references
        publicVars = {key: value for key, value in allVars.items() if not (key.startswith('_') or (isinstance(value, types.FunctionType)) or (isinstance(value,InstrumentedAttribute)))}
        return publicVars


class BaseAutoPrimary(Base):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

# Login User Loader / Session Retriever
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Define a User model


class User(UserMixin, BaseAutoPrimary):

    __tablename__ = 'user'

    # User Name
    username = db.Column(db.String(128), index=True, unique=True)

    # Identification Data: email & password
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    # Null Role refers to normal user
    privilegeId = db.Column(db.Integer, db.ForeignKey("privileges.id"))

    # Back Reference
    userPlayedPlaylist = db.relationship(
        "Results", backref="user", lazy="dynamic")

    # Password Methods
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # New instance instantiation procedure
    def __init__(self, username, email, password, role=None):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return '<User %r>' % (self.username)


class Privileges(BaseAutoPrimary):
    __tablename__ = "privileges"

    # privilege name
    name = db.Column(db.String(128), index=True, unique=True)

    # One To Many Relationship
    user = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Privileges %r>' % (self.name)

# Playlist model with track data


class Song(BaseAutoPrimary):
    spotifySongID = db.Column(db.String(100), unique=True)
    prevURL = db.Column(db.String(100))
    prevIMG = db.Column(db.String(100))
    songName = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))

    # Back Reference
    songsInPlaylist = db.relationship(
        "Playlist_Song", backref="song", lazy="dynamic")
    songsInResults = db.relationship(
        "IndividualResults", backref="song", lazy="dynamic")

    def __init__(self, spotifySongID, prevURL, prevIMG, songName, artist, album):
        self.spotifySongID = spotifySongID
        self.prevURL = prevURL
        self.prevIMG = prevIMG
        self.songName = songName
        self.artist = artist
        self.album = album

    def __repr__(self):
        return '<Song %r>' % (self.songName)


class Playlist_Song(BaseAutoPrimary):
    __tablename__ = "playlist_song"
    playlistId = db.Column(db.Integer, db.ForeignKey("playlist.id"))
    songId = db.Column(db.Integer, db.ForeignKey("song.id"))

    def __init__(self, playlist, song):
        self.playlist = playlist
        self.song = song

    def __repr__(self):
        return '<Song %r in Playlist %r>' % (self.song.songName, self.playlist.playlistName)


class Playlist(BaseAutoPrimary):
    playlistName = db.Column(db.String(100))

    # Back Reference
    playlistInSong = db.relationship(
        "Playlist_Song", backref="playlist", lazy="dynamic")
    playlistUser = db.relationship(
        "Results", backref="playlist", lazy="dynamic")

    def __init__(self, name):
        self.playlistName = name

    def __repr__(self):
        return '<Playlist %r>' % (self.playlistName)



class Results(BaseAutoPrimary):
    playlistId = db.Column(db.Integer, db.ForeignKey("playlist.id"))
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Back Reference
    resultsIndividual = db.relationship(
        "IndividualResults", backref="result", lazy="dynamic")

    def __init__(self, playlist, user):
        self.playlist = playlist
        self.user = user

    def __repr__(self):
        return '<Results %r Attempt By %r>' % (self.playlist.playlistName, self.user.username)


class IndividualResults(BaseAutoPrimary):
    __tablename__ = "individualResults"
    answerArtist = db.Column(db.String(100))
    answerSong = db.Column(db.String(100))
    isAnswerArtistCorrect = db.Column(db.Boolean)
    isAnswerSongCorrect = db.Column(db.Boolean)

    # Foreign Keys
    resultId = db.Column(db.Integer, db.ForeignKey("results.id"))
    songId = db.Column(db.Integer, db.ForeignKey("song.id"))

    def __init__(self, answerArtist, answerSong, isAnswerArtistCorrect, isAnswerSongCorrect, result, song):
        self.answerArtist = answerArtist
        self.answerSong = answerSong
        self.isAnswerArtistCorrect = isAnswerArtistCorrect
        self.isAnswerSongCorrect = isAnswerSongCorrect

        self.result = result
        self.song = song

    def __repr__(self):
        return '<IndividualResults %r By %r >' % (self.song.songName, self.result.user.username)

