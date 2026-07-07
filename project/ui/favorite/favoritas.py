from project.ui.playlist.base.music_list import ListViewMusic
import flet as ft

class Favorite(ft.Container):
    def __init__(
        self,
        list_object_music: list,
        path: str
    ):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )
        
        self.list_object_music = list_object_music
        self.path = path
        
        self.content = ListViewMusic(
            page = self.page,
            musicas = self.list_object_music,
            modo_favorita = path
        )