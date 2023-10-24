from fastapi import FastAPI, Request, HTTPException, Response
import json
import uvicorn
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util

import sqlite_helpers

app = FastAPI()

file = open("config.json")
keys = json.load(file)
client_id = keys["CLIENT_ID"]
client_secret = keys["CLIENT_SECRET"]
scope = "user-read-currently-playing"
username = "cuber322"


DATABASE_FILE_PATH = "songdatabase.db"
sqlite_helpers.maybe_create_table(DATABASE_FILE_PATH)

@app.get("/get_current_song")
async def get_current_song(request: Request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost", scope="user-read-currently-playing"))
    current_song_info = sp.current_user_playing_track()

    song = current_song_info['item']['name']
    artist = current_song_info['item']['artists'][0]['name']
    artist_uri = current_song_info['item']['artists'][0]['uri']
    artist_uri = artist_uri[15:]
    artist_details = sp.artist(artist_uri)
    genres = artist_details['genres']

    response = { "song": song, "artist": artist, "artist_uri": artist_uri, "genres": genres }
    return response

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)