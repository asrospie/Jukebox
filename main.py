import tkinter as tk
from gui import Application
from auth import user_auth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint

#username = input("Enter Spotify Username: ")

(token, cid, csec, redirect) = user_auth("ihasplaid")
root = tk.Tk()
app = Application(master=root, token=token)

app.mainloop()


#cred = SpotifyClientCredentials(client_id=cid, client_secret=csec)

#sp = spotipy.Spotify(client_credentials_manager=cred)
#result = sp.search("Radiohead")
#pprint.pprint(result)
