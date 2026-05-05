from .fonte_musica import FonteMusica
from ...Music.Repository.musica_repositorio import RepositorioMusica

class FontePlaylist(FonteMusica):
    def __init__(self, pasta : str):
        self.pasta = pasta
    
    def carregar(self):
        return RepositorioMusica._carregar_musicas(self.pasta)