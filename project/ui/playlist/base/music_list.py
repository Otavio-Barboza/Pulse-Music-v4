# import de interface
from ui.others.colors import color
from ui.playlist.containers.music_container import RowContainer

# import de back-end
from core.song.model.song import Song
from core.song.enum.song_enum import ReproductionMode
from core.song.font_reproduction.font_playlist import PlaylistFont
from core.song.controller.reproduction_manager import ReproductionManager
from core.playlists.enum.playlist_enum import PlaylistLoaded
from core.playlists.controller.playlist_state import PlaylistState
from core.favorite.enum.favorite_enum import Favorited
from core.favorite.controller.favoritas_controller import FavoriteState

# import geral
import flet as ft


class ListViewMusic(ft.ListView):
    def __init__(self, page: ft.Page, musics: list[Song], favorite_mode: ReproductionMode | None = None):
        super().__init__(
            spacing = 10,
            expand = True
        )  

        self.page = page
        self.musics = musics
        self.favorite_mode = favorite_mode

        self.controls = []
        
        self._callback = self.acutalization_container
        self._callback_qtde = self.reload
        self._callback_favoritas = self.actualization_unfavorited
        self._callback_favorita = self.actualization_favorited
        self._load()
        
        ReproductionManager.register_callback(
            event = 'actualization_container', 
            callback = self.acutalization_container
        )
        PlaylistState.register_callback(
            event = 'update_displayed_musics',
            function = self.reload
        )
        PlaylistState.register_callback(
            event = 'actualization_not_favorited',
            function = self.actualization_unfavorited
        )
        PlaylistState.register_callback(
            event = 'actualization_favorited',
            function = self.actualization_favorited
        )

        if self.favorite_mode is not None:            
            self._callback_favoritar = self.add_favorite
            self._callback_desfavoritar = self.remove_favorite

            FavoriteState.register_callback(
                event = 'add_to_favorites',
                callback = self.add_favorite
            )
            FavoriteState.register_callback(
                event = 'unfavorite',
                callback = self.remove_favorite
            )

    def will_unmount(self):        
        ReproductionManager._callbacks['actualization_container'].remove(self._callback)
        PlaylistState._callbacks['update_displayed_musics'].remove(self._callback_qtde)
        PlaylistState._callbacks['actualization_not_favorited'].remove(self._callback_favoritas)
        PlaylistState._callbacks['actualization_favorited'].remove(self._callback_favorita)
        
        if self.favorite_mode is not None:
            FavoriteState._callbacks['add_to_favorites'].remove(self._callback_favoritar)
            FavoriteState._callbacks['unfavorite'].remove(self._callback_desfavoritar)
    
    def _load(self):        
        if self.musics is None:
            return
        
        favorites_key = FavoriteState.list_favorite()

        for song in self.musics:

            if song.key in favorites_key:
                status = Favorited.FAVORITED
            else:
                status = Favorited.NOT_FAVORITED
            
            container = RowContainer(
                page = self.page,
                song = song,
                favorited_status = status
            )
            
            self.controls.append(container)
            
    def reload(self, path):        
        if (
            isinstance(PlaylistState._playlist_aberta, dict) and
            PlaylistState._playlist_aberta['open_or_close'] == PlaylistLoaded.OPEN
        ):
            try:                
                if self.favorite_mode is None:
                    font = PlaylistFont(
                        path = path,
                        mode = ReproductionMode.PLAYLIST
                    )

                    self.musics = font.load()
                    font.load_playlist(self.musics)

                ReproductionManager.update_queue_scanner()

                self.controls.clear()
                self._load()
                self.update()
            except Exception as e:
                print(f'CALLBACK RECARREGA PLATLIST ERROR: {e}')

    def add_favorite(self, data):
        if self.favorite_mode is None:
            return
        
        self.controls.append(
            RowContainer(
                page = self.page,
                song = data,
                status_favoritada = data.mode
            )
        )
        self.update()

        PlaylistState.notify(
            event = 'actualization_favorited',
            data = data.key
        )
    
    def remove_favorite(self, data):
        container_to_remove = None
        
        for container in self.controls:
            if container.data.key == data.key:
                container_to_remove = container

        self.controls.remove(container_to_remove)
        self.update()

        PlaylistState.notify(
            event = 'actualization_not_favorited',
            data = data.key
        )

    def actualization_unfavorited(self, key):
        for container in self.controls:
            if container.data.key == key:
                container.actualization_icon()
                break

    def actualization_favorited(self, key):
        for container in self.controls:
            if container.data.key == key:
                container.actualization_favrited_icon()
                break

    def acutalization_container(self, sessao: ReproductionManager):
        if not self.page:
            return
        
        for container in self.controls:
            if not container.page:
                continue

            if (
                sessao.estado.current_song is not None and
                container.data.key is not None and
                container.data.key == sessao.estado.current_song.key
            ):
                container.bgcolor = color.amarelo3
            else:
                container.bgcolor = color.preto9

            container.update()