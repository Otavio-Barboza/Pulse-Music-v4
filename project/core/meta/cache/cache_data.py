# imports de back-end
from core.meta.models.artist import Artist
from core.meta.models.album import Album

# import geral
from pathlib import Path


class CacheMetadata:

    def __init__(self):
        self.tracks: dict = {}
        self.artists = Artist()
        self.albums = Album()


    def load(self, dados_tracks: dict):
        self.tracks = dados_tracks
        self._rebuild_index()


    def _rebuild_index(self):

        self.artists = Artist()
        self.albums = Album()

        for key, data in self.tracks.items():
            # print(data)

            self.artists.add_artist(
                # Elementos da música
                key_song = key,
                path_of_song_key = Path(data.get("song_path")) / data.get("mp3_file"),

                # Elementos do artista
                artist_id = data.get('artist_id'),
                defined_artist = data.get('defined_artist')
            )
            
            # álbuns mantido nessa base ainda de operação
            self.albums.add_album(
                name = data.get("album_metadata").get("name"),
                song_path = Path(data.get("song_path")) / data.get("mp3_file"),
                song_key = key
            )