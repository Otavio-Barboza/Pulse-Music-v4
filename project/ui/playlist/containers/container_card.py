# import de interface
from ui.others.colors import color

# import de back-end
from core.services.controllers.state_app import StateApp

# import geral
import flet as ft


class PlaylistCard(ft.Container):
    def __init__(
            self, 
            on_open, 
            on_remove, 
            load_playlist,
            page: ft.Page,
            playlist_id: str, 
            name: str, 
            number_of_songs: int,
            backgroud_color: str | ft.Colors,
            backgroud_image: str,
            path: str | None,
            opacity: float = 1.0
        ):
        super().__init__(
            height = 270,
            width = 270,
            border_radius = ft.border_radius.all(20),
            scale = 1.0,
            data = {"id" : playlist_id, "path" : path},
            animate = ft.Animation(200, ft.AnimationCurve.SLOW_MIDDLE),
            on_hover = self._hover,
        )
        self.page = page
        self.playlist_name = name
        self.number_of_songs = str(number_of_songs)
        self.playlist_id = playlist_id
        self.backgroud_color = backgroud_color
        self.backgroud_image = backgroud_image
        self.opacity = opacity
        self.path = path
        self.on_open = on_open
        self.on_remove = on_remove
        self.load_playlist = load_playlist
        self.on_click = lambda e: self.load_playlist(playlist_id)

        self._image = ft.Container(
            width = 270,
            expand = True,

            content = ft.Image(
                src = self.backgroud_image,
                fit = ft.ImageFit.COVER
            )
        )
        self.name_play = self._create_text(self.playlist_name)
        self.qtde = self._create_text(f'{self.number_of_songs} músicas')

        self.information = ft.PopupMenuButton(
            icon = ft.Icons.MORE_VERT_ROUNDED,
            icon_color = color.preto3,
            surface_tint_color = color.branco,
            bgcolor = color.preto3,
            shadow_color = color.branco,
            tooltip = "Mais opções",

            style = ft.ButtonStyle(
                bgcolor = ft.Colors.TRANSPARENT,
                overlay_color = color.amarelo
            ),

            items = [
                ft.PopupMenuItem(
                    text = "Configurações Playlist",
                    data = name,
                    on_click = self.on_open
                ),

                ft.PopupMenuItem(
                    text = "Excluir Playlist",
                    data = name,                                        
                    on_click = self.on_remove
                )
            ]
        )

        self.container_information = ft.Container(
            height = 60,
            bgcolor = self.backgroud_color,

            padding = ft.padding.only(
                top = 5,
                left = 10,
                right = 10,
                bottom = 10
            ),

            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,

                controls = [
                    ft.Column(
                        spacing = 3,

                        controls = [
                            self.name_play,
                            self.qtde
                        ]
                    ),

                    self.information
                ]
            )
        )

        self.content = ft.Column(
            spacing = 0,

            controls = [
                self._image,
                self.container_information
            ]
        )

        StateApp.register_callback(
            event = 'actualization_number_songs_of_playlist',
            func = self.change_number_of_songs_in_playlist
        )

    def change_number_of_songs_in_playlist(self, number: dict):
        if not self.page:
            return
        
        if number["id"] == self.data["id"]:
            self.qtde.value = f'{number["qtde"]} músicas'
            
        try:
            self.update()
        except AssertionError as ase:
            print(ase)
            return
            
    def _create_text(self, texto : str) -> ft.Text:
        return ft.Text(
            value = texto,
            size = 16,
            overflow = ft.TextOverflow.FADE,
            color = '#ffffff',
            max_lines = 1
        )
    
    def _hover(self, e: ft.HoverEvent):
        self.scale = 1.075 if e.data == 'true' else 1.0
        self.opacity = 0.8 if e.data == 'true' else 1.0
        self.update()

    def dispose(self):
        callbacks = StateApp._callbacks.get('actualization_number_songs_of_playlist', [])
        
        if self.change_number_of_songs_in_playlist in callbacks:
            callbacks.remove(
                self.change_number_of_songs_in_playlist
            )