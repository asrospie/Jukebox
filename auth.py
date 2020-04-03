import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def user_auth(username):
    scope = "user-read-currently-playing"
    client_id = ""
    client_secret = ""
    redirect_url = ""

    try:
        creds = open("client.creds", "r")
        client_id = creds.readline().strip()
        print(client_id)
        client_secret = creds.readline().strip()
        print(client_secret)
        redirect_url = creds.readline().strip()
        print(redirect_url)
    except:
        print("Reading from credentials file was unsuccessful")
        sys.exit()

    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url)
    return token, client_id, client_secret, redirect_url
