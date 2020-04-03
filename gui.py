import tkinter as tk
from utils import currently_playing
from tkinter import font
from PIL import ImageTk, Image 
import base64
from io import BytesIO
import requests

class Application(tk.Frame):
    def __init__(self, master=None, token=0):
        super().__init__(master)
        self.master = master
        master.geometry("800x400")

        self.messageStyle = font.Font(family="Lucide Grande", size=22, weight='bold')
        self.currentSytle = font.Font(family="Lucida Grande", size=16)

        self.token = token
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        cur_p = CurrentlyPlaying(self.master, self.token)
        cur_p.grid(row=0, column=0)

        search = tk.Entry(self.master)
        search.grid(row=0, column=1, pady=2)

class CurrentlyPlaying(tk.Frame):
    def __init__(self, master=None, token=0):
        super().__init__(master=master)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.songStyle = font.Font(family="Lucida Grande", size=16)
        self.currentStyle = font.Font(family="Lucida Grande", size=20, weight='bold')
        self.token = token

        # UI elements
        # Grab the currently playing song if it exists
        song, ablum_url = currently_playing(self.token)
        if song == None:
            song = "Not Listening"
            ablum_url = "https://raw.githubusercontent.com/trianglefraternitymtu/trianglefraternitymtu.github.io/master/assets/img/COA.png"
        
        self.song_label = tk.Label(self.master, text=song, font=self.songStyle)
        current = tk.Label(self.master, text="Currently Playing", font=self.currentStyle)

        album_img = self.getImage(ablum_url)
        self.album_label = tk.Label(self.master, image=album_img)
        self.album_label.image = album_img

        current.grid(row=0, column=0, pady=2)
        self.song_label.grid(row=1, column=0, pady=2)
        self.album_label.grid(row=2, column=0, pady=2)
        self.song_label.after(5000, self.refresh_song)

    def refresh_song(self):

        # Grab the currently playing song if it exists
        song, album_url = currently_playing(self.token)
        if song == None:
            song = "Not Listening"
            album_url = "https://raw.githubusercontent.com/trianglefraternitymtu/trianglefraternitymtu.github.io/master/assets/img/COA.png"
        
        image = self.getImage(album_url)
        self.album_label.configure(image=image)
        self.album_label.image = image

        self.song_label.configure(text=song)
        self.song_label.after(5000, self.refresh_song)

    def getImage(self, url):
        response = requests.get(url)
        data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(data)).resize((200, 200), Image.ANTIALIAS))
        return img