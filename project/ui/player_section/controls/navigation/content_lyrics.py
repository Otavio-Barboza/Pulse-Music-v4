# import de interface
from ui.others.colors import color

# import de back-end
from core.lyrics.controller.lyrics_services import LyricsServices 

# import geral
import flet as ft


class LyricsContainer(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            padding = ft.padding.only(right = 30, left = 10),
            margin = ft.margin.only(bottom = 10),
            expand = True,
            alignment = ft.alignment.center
        )
        # self.page = page

        self.content = ft.Column(
            controls = [
                ft.Text(
                    value = self.load_lyric(),
                    size = 18,
                    weight = ft.FontWeight.W_500
                )
            ]
        )

        

    def did_mount(self):
        self._update_callback = self.update_lyric
        LyricsServices.register_callback(
            event = "actualization_lyric",
            callback = self.update_lyric
        )        
        
        LyricsServices.set_expanded_screen(True)

    def will_unmount(self):
        LyricsServices.set_expanded_screen(False)
        
        if self._update_callback in LyricsServices.callbacks["actualization_lyric"]:
            LyricsServices.callbacks["actualization_lyric"].remove(self._update_callback)
        
    def load_lyric(self) -> str:
        from core.lyrics.cache.cache_lyrics import CacheLyrics
        return CacheLyrics.return_lyric()
    
    def update_lyric(self, *_):
        self.content.controls[0].value = self.load_lyric()
        self.update()