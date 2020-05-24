from app import db
from app.models import *
from fuzzywuzzy import fuzz


# Used To Add Changes To Database
def commitToDatabase(item):
    db.session.add(item)
    db.session.commit()

def commitDelete(item):
    db.session.delete(item)
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

def getUsername(userId):
    return User.query.get(userId).username

def isUsernameTaken(username):
    user = User.query.filter_by(username=username.strip()).first()
    return  bool(user)

def isEmailTaken(email):
    user = User.query.filter_by(email=email.strip()).first()
    return bool(user)

def deleteUser(username):
    user = User.query.filter_by(username=username.strip()).first()
    if user:
        commitDelete(user)


def doesThisMatch(string1, string2):
    ratio = fuzz.ratio(string1.lower(), string2.lower())
    return ratio > 80



# Results Controllers
def editPlaylistName(playlistId, playlistName):
    playlist = Playlist.query.filter_by(id=playlistId).first()
    playlist.playlistName = playlistName
    db.session.commit()
    return 'success'

def getResultsOfUser(userId):
    collection = []
    userPlayedPlaylist = User.query.get(userId).userPlayedPlaylist

    # Parse all Playlist Played By User
    for playlist in userPlayedPlaylist:
        hashMap = playlist.to_dict()
        hashMap["results"] = []
        hashMap["playlistName"] = getPlaylist(playlist.playlistId).playlistName
        # Parse all the question sets in the playlist
        individualResultsCollection = playlist.resultsIndividual
        for individualResult in individualResultsCollection:
            individualResultMap = individualResult.to_dict()
            songInQuiz = Song.query.get(individualResult.songId)

            # Get Some Details of the song
            individualResultMap["correctArtist"] = songInQuiz.artist
            individualResultMap["correctSongName"] = songInQuiz.songName
            hashMap["results"].append(individualResultMap)


        collection.append(hashMap)

    return collection

# Individual Results
def addIndividualResults(userId, playlistId, songId, answerArtist, answerSong, isAnswerArtistCorrect, isAnswerSongCorrect):
    result = Results.query.filter_by(userId=userId, playlistId=playlistId).first()
    song = Song.query.get(songId)

    if (result is None):
        result = Results(Playlist.query.get(playlistId), User.query.get(userId))

    individualResults = IndividualResults(answerArtist, answerSong, isAnswerArtistCorrect, isAnswerSongCorrect, result, song)
    commitToDatabase(individualResults)
    return individualResults

# Playlist and Playlist/Song Controllers

def createNewPlaylist(playlistName):
    playlist = Playlist(playlistName)
    commitToDatabase(playlist)
    return playlist


def deletePlaylist(playlistId):
    playlist = Playlist.query.get(playlistId)
    db.session.delete(playlist)
    db.session.commit()

def getAllPlaylists():
    return Playlist.query.all()

def getPlaylist(playlistId):
    playlist = Playlist.query.get(playlistId)
    return playlist

def getPlaylistName(playlistId):
    playlist = Playlist.query.get(playlistId)
    return playlist.playlistName

def addSongInPlaylist(songId, playlistId):
    playlist = Playlist.query.get(playlistId)
    if (playlist is None):  # playlist does not exist
        raise Exception("Playlist Does Not Exist")

    # check if song already exist
    playlistSong = Playlist_Song.query.filter_by(playlistId=playlistId, songId=songId).first()

    if(playlistSong is None):
        song = Song.query.get(songId)
        addSong = Playlist_Song(playlist,song)
        commitToDatabase(addSong)

def deleteSongInPlaylist(songId,playlistId):
    playlistSong = Playlist_Song.query.filter_by(playlistId=playlistId, songId=songId).first()
    db.session.delete(playlistSong)
    db.session.commit()

def getSongsInPlaylist(playlistId):
    songs = []
    playlistSongCollection = Playlist.query.get(playlistId).playlistInSong

    for playlistSong in playlistSongCollection:
        song = playlistSong.song.to_dict()
        songs.append(song)

    return songs

def getSongDetails(songId):
    song = Song.query.get(songId)
    return song

def getSongDetailsBySpotifySongId(spotifySongId):
    return Song.query.filter_by(spotifySongID=spotifySongId).first()

def addSongDetails(spotifySongID, prevURL, prevIMG, songName, artist, album):
    song =Song.query.filter_by(spotifySongID=spotifySongID).first()
    if bool(song): # the song exist
        return song

    # The song does not exist
    newSong = Song(spotifySongID, prevURL, prevIMG, songName, artist, album)
    commitToDatabase(newSong)
    return newSong


# Deletes a Results for a Specific User result
def deleteResults(resultsId):
    results = Results.query.get(resultsId)
    individualResultsCollection = results.resultsIndividual

    for IndividualResults in individualResultsCollection:
        commitDelete(IndividualResults)

    commitDelete(results)
