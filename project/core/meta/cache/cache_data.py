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
            print(data)

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

    # def update_artists(
    #     self,
    #     track_id: str,
    #     new_artist_id: str,
    #     new_name: str,
    #     new_image: str
    # ):
    #     track = self.tracks[track_id]

    #     previous_artist = track["artist_metadata"]["id_deezer"]

    #     track["artist_metadata"]["id_deezer"] = new_artist_id
    #     track["defined_artist"] = new_name
    #     track["artist_metadata"]["big"] = new_image

    #     self.artists.remove(track_id, previous_artist)
    #     self.artists.add_artist(
    #         track_id,
    #         new_artist_id,
    #         new_name,
    #         new_image
    #     )