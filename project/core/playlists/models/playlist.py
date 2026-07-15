from core.playlists.models.playlist_config import PlaylistConfig


class Playlist:
    def __init__(
        self, 
        id : str, 
        name : str, 
        path : str = ''
    ):
        self.id = id
        self.name = name
        self.path = path
        self._config = None

    def carregar_config(self):
        if self._config is None:
            self._config = PlaylistConfig.carregar(self.caminho)
        return self._config