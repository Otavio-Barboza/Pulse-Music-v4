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
            bgcolor = '#f9f9f9'
        )
        
        self.page = page
        self.listas_objetos_musicas = lista_objetos_musica
        self.caminho = caminho
        
        self.content = ListViewMusicas(
            page = self.page,
            musicas = lista_objetos_musica,
            pasta_musicas = caminho
        )