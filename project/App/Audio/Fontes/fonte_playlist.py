from .fonte_reproducao import FonteReproducao
from ..Repository.musica_repositorio import RepositorioMusica
from ..Model.modo_reproducao import Reprodução

class FontePlaylist(FonteReproducao):
    def __init__(self, modo, pasta : str):
        self.modo = modo
        self.pasta = pasta
    
    def carregar(self) -> list:
        return RepositorioMusica._carregar_musicas(
            pasta = self.pasta,
            modo = self.modo
        )
    
    def carregar_playlist(self, lista_musicas):
        Reprodução.carregar_musicas_do_modo(
            modo = self.modo, 
            lista = lista_musicas
        )