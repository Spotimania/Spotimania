from app.controllers import *
from flask import Blueprint, request, jsonify, abort, Response
api =Blueprint("api",__name__)

@api.route("/")
def test():
    return ({"message": "Hello World"})

@api.route("/playlist/<playlistId>", methods=['POST'])
def routeAddSongsInPlaylist(playlistId):
    try:
        print(request.data)
        body = request.get_json(force=True)
        print(body)
        song = addSongDetails(body["spotifySongID"], body["prevURL"], body["prevIMG"], body["songName"], body["artist"], body["album"])
        addSongInPlaylist(song.id,playlistId)
        return ({"message": "Success!"})
    except Exception as err:
        abort(Response("Something Went Wrong"))

@api.route("/playlist/<playlistId>", methods=['PUT'])
def routeEditPlaylistName(playlistId):
    try:
        body = request.get_json(force=True)
        editPlaylistName(playlistId,body["playlistName"])
        return ({"message": "Success!"})
    except Exception as err:
        abort(Response("Something Went Wrong"))


@api.route("/playlist/<playlistId>/<spotifySongId>", methods=['DELETE'])
def routeDeleteSongsInPlaylist(playlistId, spotifySongId):
    songId = getSongDetailsBySpotifySongId(spotifySongId).id
    try:
        deleteSongInPlaylist(songId, playlistId)
        return ({"message": "Success!"})
    except Exception as err:
        abort(Response("Something Went Wrong"))