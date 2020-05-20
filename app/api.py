from app.controllers import *
from flask import Blueprint, request, jsonify, abort, Response
api =Blueprint("api",__name__)

@api.route("/")
def test():
    return ({"message": "Hello World"})

@api.route("/playlist/<playlistId>", methods=['POST'])
def routeAddSongsInPlaylist(playlistId):
    try:
        body = request.get_json()
        song = addSongDetails(body["songID"], body["prevURL"], body["prevIMG"], body["songName"], body["artist"], body["album"])
        addSongInPlaylist(song.id,playlistId)
        return ({"message": "Success!"})
    except:
        abort(Response("Something Went Wrong"))


@api.route("/playlist/<playlistId>/<songId>", methods=['DELETE'])
def routeDeleteSongsInPlaylist(playlistId, songId):
    try:
        deleteSongInPlaylist(songId, playlistId)
        return ({"message": "Success!"})
    except:
        abort(Response("Something Went Wrong"))