from fastapi import FastAPI, Request, HTTPException, Response
import json
import uvicorn
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

import sqlite_helpers

app = FastAPI()

file = open("config.json")
keys = json.load(file)
client_id = keys["CLIENT_ID"]
client_secret = keys["CLIENT_SECRET"]
scope = "user-read-currently-playing"

# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost", scope=scope))

file = open(".cache")
token_info = json.load(file)
token = token_info["access_token"]

sp = spotipy.Spotify(auth=token)

current_playback = sp.current_playback()

# Check if the user is currently playing a track
if current_playback is not None and 'item' in current_playback:
    track = current_playback['item']
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    print(f"Currently playing: {track_name} by {artist_name}")
else:
    print("No track is currently playing.")
























DATABASE_FILE_PATH = "songdatabase.db"
sqlite_helpers.maybe_create_table(DATABASE_FILE_PATH)

@app.get("/get_current_song")
async def get_current_song(request: Request):
    current_song = sp.current_playback()
    print(current_song['item']['name'])
