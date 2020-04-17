class SpotifyObj:
    def __init__(self, song, artists, album, uri):
        self.song = song
        self.artists = artists
        self.album = album
        self.uri = uri

    def get_song(self):
        return self.song

    def get_artists(self):
        return self.artists

    def get_album(self):
        return self.album

    def get_uri(self):
        return self.uri
