# import de back-end
from core.playlists.models.playlist_config import PlaylistConfig

# import geral
from pathlib import Path


class Playlist:
    def __init__(
        self, 
        id: str, 
        name: str, 
        path: Path
    ):
        self.id = id
        self.name = name
        self.path = path
        self._config = None

    def carregar_config(self):
        if self._config is None:
            self._config = PlaylistConfig.load(self.path)
        return self._config