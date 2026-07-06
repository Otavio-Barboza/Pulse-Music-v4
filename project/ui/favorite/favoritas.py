from ..Playlist.Base.list_musicas import ListViewMusicas
import flet as ft

class Favoritas(ft.Container):
    def __init__(
        self,
        page : ft.Page,
        lista_objetos_musica : list,
        caminho : str
    ):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )
        
        self.page = page
        self.listas_objetos_musicas = lista_objetos_musica
        self.caminho = caminho
        
        self.content = ListViewMusicas(
            page = self.page,
            musicas = self.listas_objetos_musicas,
            modo_favorita = caminho
        )