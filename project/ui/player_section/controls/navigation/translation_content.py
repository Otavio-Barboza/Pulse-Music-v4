# import de interface
from ui.others.colors import color

# import de back-end
from core.lyrics.controller.lyrics_services import LyricsServices

# import geral
import flet as ft


class TranslationContent(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            padding = ft.padding.only(right = 30, left = 10),
            margin = ft.margin.only(bottom = 10),
            expand = True,
            alignment = ft.alignment.center
        )
        self.page = page

        self.information = ft.PopupMenuButton(
            icon = ft.Icons.G_TRANSLATE,
            icon_color = color.preto3,
            surface_tint_color = color.branco,
            bgcolor = color.preto3,
            shadow_color = color.branco,
            tooltip = "Idiomas",

            style = ft.ButtonStyle(
                color = {
                    ft.ControlState.DEFAULT : color.azul_medio2,
                    ft.ControlState.HOVERED : color.azul_medio
                },
                overlay_color = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.DEFAULT : color.branco
                }
            ),

            items = [
                ft.PopupMenuItem(
                    text = language,
                    data = {
                        'uf' : uf,
                        'language' : language
                    },                                        
                    on_click = self.select_language
                ) for language, uf in LyricsServices.AVAILABLE_LANGUAGES.items()
            ]
        )

        self.lyric = ft.Container(
            alignment = ft.alignment.center,
            expand = True,
            
            content = ft.Text(
                size = 18,
                weight = ft.FontWeight.W_500,

                value = self.load_lyric()
            )
        )

        self.content = ft.Column(
            expand = True,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.Row(
                    height = 75,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 30,
                    controls = [
                        ft.Text(
                            value = 'Selecione um language',
                            size = 26,
                            weight = ft.FontWeight.BOLD
                        ),
                        self.information
                    ]
                ),
                self.lyric
            ]
        )

    def load_lyric(self):
        from project.core.lyrics.cache.cache_lyrics import CacheLyrics

        if CacheLyrics.cache_lyrics is None:
            return 'Nenhuma lyric carregada para tradução'
        else:
            return LyricsServices.start_translation(CacheLyrics.cache_lyrics)

    def select_language(self, e):
        from project.core.lyrics.cache.cache_lyrics import CacheLyrics

        CacheLyrics.update_cache(e.control.data.get('language'))
        LyricsServices.translator.target = e.control.data.get('uf')
        
        self.lyric.content.value = LyricsServices.start_translation(e.control.data.get('language'))
        self.update()