from project.ui.playlist.base.music_list import ListViewMusic
import flet as ft

class Favorite(ft.Container):
    def __init__(
        self,
        lista_objetos_musica: list,
        caminho: str
    ):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )
        
        self.listas_objetos_musicas = lista_objetos_musica
        self.caminho = caminho
        
        self.content = ListViewMusic(
            page = self.page,
            musicas = self.listas_objetos_musicas,
            modo_favorita = caminho
        )