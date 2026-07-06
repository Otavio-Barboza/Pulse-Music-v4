from .playlist_config import PlaylistConfig

class Playlist:
    def __init__(
            self, 
            id : str, 
            nome : str, 
            tipo : str,
            caminho : str = ''
        ):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.caminho = caminho
        self._config = None

    def carregar_config(self):
        if self._config is None:
            self._config = PlaylistConfig.carregar(self.caminho)
        return self._config