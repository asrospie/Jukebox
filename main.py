import tkinter as tk
from gui import Application
from auth import user_auth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
from utils import search_song

#username = input("Enter Spotify Username: ")
(token, cid, csec, redirect) = user_auth("ihasplaid")
manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
sp = spotipy.Spotify(auth=token)
root = tk.Tk()
app = Application(master=root, token=token, sp=sp)

app.mainloop()
