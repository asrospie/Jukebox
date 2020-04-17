import pprint
import requests
import json
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotify_obj import SpotifyObj

def currently_playing(token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.get(url, headers=headers)
    if response.text == "":
        return None, None
    json_data = json.loads(response.text)
    song = json_data["item"]["name"]
    album_url = json_data["item"]["album"]["images"][1]["url"]
    return song, album_url


# Returns a list of songs given the search query, capped at 10
def search_song(query: str, sp: spotipy.Spotify):
    result = sp.search(query)
    ret = []
    for item in result["tracks"]["items"]:
        song = item["name"]
        artists = []
        for i in item["artists"]:
            artists.append(i["name"])
        uri = item["uri"]
        album = item["album"]["name"]
        temp = SpotifyObj(song, artists, album, uri) 
        ret.append(temp)
    return ret

# Used to start the playback of a song
def queue_song(uri: str, sp: spotipy.Spotify):
    sp.add_to_queue(uri=uri)