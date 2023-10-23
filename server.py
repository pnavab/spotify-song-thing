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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost", scope="user-read-currently-playing"))

print("--------------------------")
result = sp.current_user_playing_track()
print(result)
print(result['item']['name'])
artist = result['item']['artists'][0]['name']
print(f"by {artist}")
print("--------------------------")


DATABASE_FILE_PATH = "songdatabase.db"
sqlite_helpers.maybe_create_table(DATABASE_FILE_PATH)

@app.get("/get_current_song")
async def get_current_song(request: Request):
    current_song = sp.current_user_playing_track()
    print(current_song['item']['name'])
