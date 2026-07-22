# import de interface
from ui.others.colors import color

# import de back-end
from core.services.controllers.state_app import StateApp
from core.playlists.controller.playlist_state import PlaylistState
from core.favorite.controller.favoritas_controller import FavoriteState
from core.favorite.enum.favorite_enum import Favorited
from core.song.enum.song_enum import ReproductionMode
from core.song.model.reproduction import Reproduction
from core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class RowContainer(ft.Container):
    def __init__(
            self, 
            page,
            song, 
            favorited_status
        ):
        super().__init__(
            border_radius = ft.border_radius.all(10),
            height = 55,
            bgcolor = color.preto9,
            padding = ft.padding.all(5),
            alignment = ft.alignment.center,
            data = song,
            on_click = self.play_or_pause
        )
        self.page = page
        self._is_favorited = favorited_status
        self.data = song
        self.src_cover = self.return_cover()

        self.icon = ft.IconButton(
            data = song,
            icon = self.is_favorited(),

            style = ft.ButtonStyle(
                color = color.rosa_avermelhado,

                overlay_color = {
                    ft.ControlState.HOVERED : color.cinza2
                }
            ),
            
            on_click = self.toggle_favorited 
        )

        self.cover_image = ft.Image(
            src = self.src_cover,
            border_radius = ft.border_radius.all(5),
            fit = ft.ImageFit.COVER,
            filter_quality = ft.FilterQuality.MEDIUM,
            height = 47.5,
            width = 80
        )

        self.song_name = self._create_text(
            name = self.data.name, 
            size = 900
        )
        self.artist_name = self._create_text(
            name = self.return_artist(), 
            size = 300
        )
        
        self.content = ft.Row(
            spacing = 40,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.SPACE_AROUND,

            controls = [
                self.icon,
                self.cover_image,

                ft.Row(
                    wrap = True,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.START,
                    run_alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 10,
                    run_spacing = 1,
                    expand = True,
                    
                    controls = [
                        self.song_name,
                        self.artist_name
                    ]
                )
            ]
        )

        self._callback_artists = self.update_artists
        self._callback_covers = self.update_covers

        StateApp.register_callback(
            event = 'actualization_artist',
            func = self.update_artists
        )
        StateApp.register_callback(
            event = 'actualization_cover',
            func = self.update_covers
        )

    def will_unmount(self):
        StateApp._callbacks['actualization_artist'].remove(self._callback_artists)
        StateApp._callbacks['actualization_cover'].remove(self._callback_covers)

    def _create_text(self, name: str, size: int):
        return ft.Text(
            value = name,
            size = 15,
            weight = ft.FontWeight.W_500,
            overflow = ft.TextOverflow.ELLIPSIS,
            max_lines = 1,
            text_align = ft.TextAlign.LEFT,
            width = size
        )
    
    def is_favorited(self):          
        if self._is_favorited == Favorited.NOT_FAVORITED:
            return ft.Icons.FAVORITE_ROUNDED
        else:
            return ft.Icons.HEART_BROKEN_ROUNDED

    def actualization_icon(self):
        self._is_favorited = Favorited.NOT_FAVORITED
        self.icon.icon = ft.Icons.HEART_BROKEN_ROUNDED
        self.icon.update()
    
    def actualization_favrited_icon(self):
        self._is_favorited = Favorited.FAVORITED
        self.icon.icon = ft.Icons.FAVORITE_ROUNDED
        self.icon.update()
    
    def toggle_favorited(self, e):        
        if self._is_favorited == Favorited.FAVORITED:
            self._is_favorited = Favorited.NOT_FAVORITED
            self.icon.icon = ft.Icons.HEART_BROKEN_ROUNDED
            self.unfavorite(e.control.data)
        else:
            self._is_favorited = Favorited.FAVORITED
            self.icon.icon = ft.Icons.FAVORITE
            self.favorite(e.control.data)

        if self.page:
            self.icon.update()
        
    def favorite(self, data):
        FavoriteState.convert_object_to_json(data)
        FavoriteState.add_music_to_playback(data)
        ReproductionManager.update_queues()

    def unfavorite(self, data):
        FavoriteState.remove_favorite_json(data)
        FavoriteState.remove_music_to_playback(data)
        ReproductionManager.update_queues()

    def play_or_pause(self, e):
        if Reproduction.current_reproduction != e.control.data.modo:
            if e.control.data.modo == ReproductionMode.FAVORITE.value:
                Reproduction.set_current_reproduction(ReproductionMode.FAVORITE)
            else:
                Reproduction.set_current_reproduction(e.control.data.modo)
        
        if ReproductionManager.fonte_atual != e.control.data.modo:
            ReproductionManager.set_font()

        if ReproductionManager.current_font is ReproductionMode.NOT_REPRODUCE:
            print('Sem reprodução definida')
            return

        ReproductionManager.get_index(e.control.data.chave)
        ReproductionManager.play()

    def return_artist(self) -> str:
        return PlaylistState.return_music_artist(self.data.key)
    
    def return_cover(self) -> str:
        return PlaylistState.return_cover(self.data.name)
    
    def update_artists(self, _):
        name = self.return_artist()
        self.artist_name.value = name
        
        try:
            if self.page:
                self.artist_name.update()
        except Exception as e:
            print(f'CALLBACK ARTISTAS ATT ERROR: {e}')

    def update_covers(self, _):
        cover_destination = self.return_cover()
        self.cover_image.src = cover_destination
        
        try:
            if self.page:
                self.cover_image.update()
        except Exception as e:
            print(f'CALLBACK CAPAS ATT ERROR: {e}')