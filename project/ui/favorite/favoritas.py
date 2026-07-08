# import de interface
from project.ui.playlist.base.music_list import ListViewMusic

# import de back-end
from project.core.song.model.song import Song
from project.core.song.enum.song_enum import ReproductionMode

# import geral
import flet as ft


class Favorite(ft.Container):
    def __init__(
        self,
        list_music_object: list[Song],
        favorite_mode: ReproductionMode
    ):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )
        
        self.list_music_object = list_music_object
        self.favorite_mode = favorite_mode
        
        self.content = ListViewMusic(
            musicas = self.list_music_object,
            modo_favorita = favorite_mode
        )