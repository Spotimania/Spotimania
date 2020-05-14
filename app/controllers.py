from app import db
from app.models import *


# Used To Add Changes To Database
def commitToDatabase(item):
    db.session.add(item)
    db.session.commit()

# User Controllers
def getAdminRole():
    adminRole = Privileges.query.filter_by(name="Administrator").first()
    if (adminRole):
        return adminRole
    adminRole = Privileges("Administrator")
    commitToDatabase(adminRole)
    return adminRole

def createNewUser(username, password, email):
    user = User(username.strip(), email.strip(),password.strip())
    commitToDatabase(user)
    return user

def createNewAdmin(username, password, email):
    adminRole = getAdminRole()
    user = User(username.strip(), email.strip(),password.strip(),adminRole)
    commitToDatabase(user)
    return user

# Gets The User Object Once Validated, otherwise returns false
def validateUserLogin(username, password):
    user = User.query.filter_by(username=username.strip()).first()
    if (user and user.check_password(password)):
        return user

    return False

def isUsernameTaken(username):
    user = User.query.filter_by(username=username.strip()).first()
    return  bool(user)

def isEmailTaken(email):
    user = User.query.filter_by(email=email.strip()).first()
    return bool(user)


def editPlaylistName(playlistId, playlistName):
    playlist = Playlist.query.filter_by(playlistId=playlistId).first()
    playlist.playlistName = playlistName
    db.session.commit()
    return 'success'

def deletePlaylist(playlistId):
    playlist = Playlist.query.filter_by(playlistId=playlistId).first()
    db.session.delete(playlist)
    db.session.commit()
    return 'success'

def getPlaylistName(playlistId):
    playlist = Playlist.query.filter_by(playlistId=playlistId).first()
    return playlist.name

def addSongInPlaylist(songId,playListId):
    addSong = Playlist_Song(songId, playlistId)
    db.session.add(addSong)
    db.session.commit()

def deleteSongInPlaylist(songId,playListId):
    playlistSong = Playlist_Song.query.filter_by(playlistId=playlistId, songId=songId).first()
    db.session.delete(playlistSong)
    db.session.commit()

def getSongsInPlaylist(playlistId):
    songs = []
    playlistSong = Playlist_Song.query.filter_by(playlistId=playlistId).all()
    for playlist in playlistSong:
        songs.append(playlist.)