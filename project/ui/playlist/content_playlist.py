# imports de interface
from ui.playlist.overlay import ContainerOverlay
from ui.playlist.base.grid_playlists import GridPlaylists
from ui.playlist.base.music_list import ListViewMusic
from ui.others.colors import color

# imports de back-end
from core.playlists.enum.playlist_enum import PlalistOverlayMode, PlaylistLoaded
from core.playlists.controller.playlist_manager import PlaylistManager
from core.playlists.controller.playlist_state import PlaylistState
from core.song.font_reproduction.font_playlist import PlaylistFont
from core.song.enum.song_enum import ReproductionMode

# import geral
import flet as ft


class ContentPlaylist(ft.Container):
    def __init__(self, open_function):
        super().__init__(
            padding = ft.padding.all(10),
            expand = True
        )

        self.open_function = open_function

        self.grid: ft.GridView = GridPlaylists(
            on_open = self.abrir_config_playlist,
            on_remove = self._remove_playlist,
            load_songs = self.open_playlist
        )
        self.state = PlaylistManager(self.grid)
        
        self.content = self.grid

    def load(self):
        """
            Carrega os Cards na tela na inicialização do player
        """
        self.state.load_playlists()
        self.update()

    def abrir_config_playlist(self, e):
        self.state.open_config_playlist(e)
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                state = self.state,
                modo = PlalistOverlayMode.UPDATE
            ) 
        )
        self.page.update()
    
    def _remove_playlist(self, playlist_id : str):        
        """
            Ordem: PlaylistManager -> Grid & Repositorio -> CreatePlaylist
        Args:
            playlist_id (str): ID da playlist
        """

        self.state.remove_playlist(playlist_id)

    def _create_playlist(self):
        """
            Ordem: Estadoplaylist -> Grid & Repositorio -> CreatePlaylist
        """
        
        self.state.create_playlist()
        
    def open_playlist(self, id : str, data : str):
        """
            Ordem: PlaylistManager ->
        Args:
            id (str): ID da playlist
        """

        card = self.grid.cards[id]

        fonte = PlaylistFont(
            path = card.pasta,
            mode = ReproductionMode.PLAYLIST
        )
        
        list_music = fonte.load()
        
        fonte.load_playlist(
            lista_musicas = list_music
        )

        self.open_function()

        list_view = ListViewMusic(
            page = self.page,
            musics = list_music,
            favorite_mode = None
        )
        
        self.content = list_view
        self.update()

        PlaylistState.open_playlist(
            id = card.data['id'],
            status = PlaylistLoaded.OPEN
        )
        
    def close_playlist(self):        
        self.content = self.grid
        self.update()

        PlaylistState.close_playlist()