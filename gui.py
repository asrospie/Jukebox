import tkinter as tk
from utils import currently_playing
from utils import search_song
from utils import queue_song
from spotify_obj import SpotifyObj
from tkinter import font
from PIL import ImageTk, Image 
import base64
from io import BytesIO
import requests

class Application(tk.Frame):
    def __init__(self, master=None, token=0, sp=None):
        super().__init__(master)
        self.master = master
        master.geometry("800x480")

        self.sp = sp

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

        # search = tk.Entry(self.master)
        # search.grid(row=0, column=1, pady=2)
        search_sec = Search(self.master, self.sp)
        search_sec.grid(row=0, column=1, pady=2)

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

        current.grid(row=0, column=0)
        self.song_label.grid(row=1, column=0)
        self.album_label.grid(row=2, column=0)
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

class Search(tk.Frame):
    def __init__(self, master=None, sp=None):
        super().__init__(master=master)

        # utility data 
        self.cur_list = []
        self.popups = 0

        # Grid setup 
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Spotipy requirements
        self.sp = sp

        # UI Elements
        self.inner_grid = tk.Frame(self.master)
        self.search = tk.Entry(self.inner_grid)
        self.s_button = tk.Button(self.inner_grid, state="normal", text="Go", command=lambda: self.run_search(self.search.get()))
        self.q_box = tk.Listbox(self.master)

        self.q_box.bind('<<ListboxSelect>>', self.on_select)

        # Add UI Elements to the grid
        self.search.grid(row=0, column=0, pady=2)
        self.s_button.grid(row=0, column=2)
        self.inner_grid.grid(row=0, column=1, pady=2)
        self.q_box.grid(row=1, column=1, rowspan=2)

    # Function to run the search and insert a song into the q_box
    def run_search(self, query=None):
        if query == None or query == "":
            return
        results = search_song(query, self.sp)
        self.q_box.delete(0, tk.END)
        self.cur_list = []
        for i in results:
            temp = i.get_song() + " - " + i.get_artists()[0]
            self.q_box.insert(tk.END, temp)
            self.cur_list.append(i)
        self.master.update()

    # Function to run the on_select in the q_boxk
    def on_select(self, event):
        # TEMPORARY SOLUTION TO ONE FRAME AT A TIME

        w = event.widget
        selection = w.curselection()
        if not selection:
            return
        idx = int(w.curselection()[0])
        
        if idx < 0 or idx >= len(self.cur_list):
            return

        print("-------------")
        print("SONG: ", self.cur_list[idx].get_song())
        print("ARTIST: ", self.cur_list[idx].get_artists()[0])
        print("ALBUM: ", self.cur_list[idx].get_album())
        print("URI: ", self.cur_list[idx].get_uri())
        print("-------------")

        obj = self.cur_list[idx]

        # Create add song to queue popup
        popup = tk.Toplevel()
        popup.geometry("800x480")
        temp_msg = tk.Label(popup, text="Hello World!")
        temp_msg.pack()

        queue_btn = tk.Button(popup, text="Request Song", command=lambda: self.request_song(obj, popup)) 
        queue_btn.pack()

        close_btn = tk.Button(popup, text="Close", command=lambda: self.destroy_release(popup))
        close_btn.pack()
        popup.grab_set()
        popup.mainloop()

    def request_song(self, obj, popup):
        queue_song(obj.get_uri(), self.sp)
        self.destroy_release(popup)

    def destroy_release(self, popup):
        popup.grab_release()
        popup.destroy()