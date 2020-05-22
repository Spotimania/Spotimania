from app.controllers import *
from app import socketio
from flask import render_template, session, request, \
    copy_current_request_context, jsonify,json
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# sharedVar Strucure:
# -> dict: playerRooms: rooms, [playerIds]
# -> dict: roomPlaylist, playlistId
# -> dict: playerId, score
# ->

global playerRooms
global scores
global roomPlaylist
global songs
global songsFiltered
global currentSongIndex
playerRooms = {}
scores = {}
roomPlaylist = {}
songs = {}
songsFiltered = {}
currentSongIndex={}

#SOCKETS
@socketio.on('connectFirstTime', namespace='/sockets')
def connectFirstTime(message):
    # sharedVar setters

    if not(message['room']  in playerRooms):
        playerRooms[message['room']] = []
        roomPlaylist[message['room']]= message['playlistId']


    # add only unique players
    if(not(message['userId'] in playerRooms[message['room']] )):
        playerRooms[message['room']]+=message['userId']
    print(playerRooms[message['room']])

    # RESET USER SCORE
    scores[message['userId']] = 0

    join_room(message['room'])
    emit('onUserJoin',{'username': message['username'],'userId': message['userId']},room=message['room'])

    # SEND A PACKAGED SYNCING OF USERS
    def sendUserDetails():
        print("SENDING USER DETAILS")
        # GET ALL USERS OF THE ROOM
        allUserIds = playerRooms[message['room']]
        print(allUserIds)
        # MAP CALLBACK FUNCTION
        def getDictUserIdsAndName(userId):
            username = getUsername(userId)
            return  {"username":username,"userId":userId}

        users = list(map(getDictUserIdsAndName,allUserIds))
        print(users)
        emit("syncUsers", users, room=message['room'])

    sendUserDetails()

@socketio.on('startGame', namespace='/sockets')
def startGame(message):
    room = message["room"]
    playlistId =roomPlaylist[room]

    songs[room] = getSongsInPlaylist(playlistId)
    songsFiltered[room] = getSongsInPlaylist(playlistId)
    currentSongIndex[room] = 1

    for song in songsFiltered[room]:
        del song["songName"]
        del song["artist"]
        del song["date_created"]
        del song["date_modified"]
        del song["spotifySongID"]
    emit('receivesSongData', songsFiltered[room][0], room=room)



@socketio.on('nextSong', namespace='/sockets')
def nextSong(message):
    room = message["room"]
    print(room)
    currentSongIndexLocal = currentSongIndex[room]

    # END OF THE SONG
    songFiltered = songsFiltered[room]
    if (len(songFiltered) <= currentSongIndexLocal):
        print("END OF SONG")
    else:
        currentSongFiltered = songFiltered[currentSongIndexLocal]
        emit('receivesSongData',currentSongFiltered,room=room)
        currentSongIndex[room] += 1

@socketio.on("submitAnswer", namespace='/sockets')
def submitAnswer(message):
    print(message["artist"])
    print(message["song"])
    print(message["userId"])
    print(message["room"])
    print(message["songId"])

    userId=message["userId"]
    username = getUsername(userId)
    playlistId =roomPlaylist[message["room"]]
    song = getSongDetails(message["songId"])
    print(song.songName)
    print(song.artist)
    isAnswerArtistCorrect = doesThisMatch(message["artist"],song.artist)
    isAnswerSongCorrect = doesThisMatch(message["song"], song.songName)

    print(isAnswerArtistCorrect)
    print(isAnswerSongCorrect)

    #CONSTANTS
    CORRECT_SONG_POINTS = 5
    CORRECT_ARTIST_POINTS = 5
    score = isAnswerArtistCorrect *CORRECT_SONG_POINTS + isAnswerSongCorrect*CORRECT_ARTIST_POINTS
    scores[message['userId']] += score

    # DATA BASE STORAGE
    addIndividualResults(userId,playlistId,song.id,message["artist"],message["song"],isAnswerArtistCorrect,isAnswerSongCorrect)

    emit('receivesScoreData',{"scoreReceived":score,"newScore": scores[message['userId']],"username":username,'userId': message['userId']},room=message['room'])

@socketio.on('disconnect', namespace='/sockets')
def test_disconnect():
    print('Client disconnected', request.sid)