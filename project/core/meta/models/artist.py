class Artist:

    def __init__(self):
        self.artist: dict[str, list[dict[str]]] = {}

    def add_artist(
        self,
        key_song: str,
        path_of_song_key : str ,
        artist_id: str | None,
        defined_artist : str
    ):

        if not artist_id or not key_song:
            return  
        
        if artist_id not in self.artist:
            self.artist[artist_id] = {
                'defined_artist' : defined_artist,
                'songs': []
            }

        self.artist[artist_id]["songs"].append({
            'key' : key_song, 
            'artist_path' : path_of_song_key
        })

    def remove(self, track_id: str, artist_id: str | None):
        if not artist_id:
            return

        if artist_id not in self.artist:
            return

        lista = self.artist[artist_id]["songs"]

        if track_id in lista:
            lista.remove(track_id)

        if not lista:
            del self.artist[artist_id]

    def to_dict(self):
        return self.artist