from app.controllers import *
from app import socketio
from flask import render_template, session, request, \
    copy_current_request_context, jsonify,json
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# SessionStrucure:
# -> dict: playerRooms: rooms, [playerIds]
# -> dict: roomPlaylist, playlistId
# -> dict: playerId, score
# ->

#SOCKETS
@socketio.on('connectFirstTime', namespace='/sockets')
def connectFirstTime(message):
    if not("playerRooms" in session):
        session["playerRooms"] = {}
    if not("scores" in session):
        session["scores"] = {}
    if not("roomPlaylist" in session):
        session["roomPlaylist"] = {}

    print(message)
    print(message['room'])
    print(message['userId'])
    print(message['username'])
    print(message['playlistId'])
    # CHECK IF ROOM ALREADY EXIST
    if message['room'] in session["playerRooms"]:
        session["playerRooms"][message['room']].append(message['userId'])
    else:
        session["playerRooms"][message['room']] = [message['userId']]
        session["roomPlaylist"][message['room']]= message['playlistId']

    # RESET USER SCORE
    session["scores"]["playerId"] = 0

    session[message["username"]] = 0;
    join_room(message['room'])
    emit('onUserJoin',{'username': message['username']},room=message['room'])

@socketio.on('startGame', namespace='/sockets')
def startGame(message):
    room = message["room"]
    playlistId = session["roomPlaylist"][room]

    session["songs"] = {}
    session["songsFiltered"] = {}
    session["songs"][room] = getSongsInPlaylist(playlistId)
    session["songsFiltered"][room] = getSongsInPlaylist(playlistId)
    session["currentSongIndex"] = {}
    session["currentSongIndex"][room] = 1

    for song in session["songsFiltered"][room]:
        del song["songName"]
        del song["artist"]
        del song["date_created"]
        del song["date_modified"]
        del song["spotifySongID"]
    jsonDump = json.dumps(session["songsFiltered"][room])
    print(jsonDump)
    print(jsonify(jsonDump))
    emit('receivesSongData',session["songsFiltered"][room][0],room=message['room'])


@socketio.on('leave', namespace='/sockets')
def leave(message):
    leave_room(message['room'])
    emit('my_response',
         {'data': 'Left rooms: ' + ', '.join(rooms())})

@socketio.on('my_room_event', namespace='/sockets')
def send_room_message(message):
    emit('my_response',{'data': message['data'] + " By: " + str(message["userId"]) + " *score = " + str(session[str(message["userId"])])},room=message['room'])

@socketio.on('disconnect', namespace='/sockets')
def test_disconnect():
    print('Client disconnected', request.sid)