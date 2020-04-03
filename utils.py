import requests
import json

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