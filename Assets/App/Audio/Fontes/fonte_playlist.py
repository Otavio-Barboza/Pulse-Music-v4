from .fonte_reproducao import FonteReproducao
from ..Repository.musica_repositorio import RepositorioMusica

class FontePlaylist(FonteReproducao):
    def __init__(self, pasta : str):
        self.pasta = pasta
    
    def carregar(self):
        return RepositorioMusica._carregar_musicas(self.pasta)