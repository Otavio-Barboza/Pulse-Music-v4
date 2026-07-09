# imports de interface
from project.ui.playlist.overlay import ContainerOverlay
from project.ui.playlist.base.grid_playlists import GridPlaylists
from project.ui.playlist.base.music_list import ListViewMusic
from project.ui.others.colors import color

# imports de back-end
from project.core.playlists.enum.playlist_enum import PlalistOverlayMode, PlaylistLoaded
from project.core.playlists.controller.playlist_manager import PlaylistManager
from project.core.playlists.controller.playlist_state import PlaylistState
from project.core.song.font_reproduction.font_playlist import PlaylistFont
from project.core.song.enum.song_enum import ReproductionMode

# import geral
import flet as ft

class ContentPlaylist(ft.Container):
    def __init__(self, abrir):
        super().__init__(
            padding = ft.padding.all(10),
            expand = True
        )

        self.abrir = abrir

        self.grid: ft.GridView = GridPlaylists(
            page = self.page,
            on_abrir = self.abrir_config_playlist,
            on_remover = self._remover_playlist,
            carregar_musicas = self.abrir_playlist
        )
        self.estado = PlaylistManager(self.grid)
        
        self.content = self.grid

    def carregar(self):
        """
            Carrega os Cards na tela na inicialização do player
        """
        self.estado.carregar_playlists()
        self.update()

    def abrir_config_playlist(self, e):
        self.estado.abrir_config_playlist(e)
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                estado = self.estado,
                conteudo = self,
                modo = PlalistOverlayMode.UPDATE
            ) 
        )
        self.page.update()
    
    def _remover_playlist(self, playlist_id : str):        
        """
            Ordem: PlaylistManager -> Grid & Repositorio -> CreatePlaylist
        Args:
            playlist_id (str): ID da playlist
        """

        self.estado.remover_playlist(playlist_id)

    def _criar_play(self):
        """
            Ordem: Estadoplaylist -> Grid & Repositorio -> CreatePlaylist
        """
        
        self.estado.criar_playlist()
        
    def abrir_playlist(self, id : str, data : str):
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
        
        lista_de_musicas = fonte.carregar()
        
        fonte.carregar_playlist(
            lista_musicas = lista_de_musicas
        )

        self.abrir()

        list_view = ListViewMusic(
            page = self.page,
            musicas = lista_de_musicas,
            modo_favorita = None
        )
        
        self.content = list_view
        self.update()

        PlaylistState.open_playlist(
            id = card.data['id'],
            status = PlaylistLoaded.OPEN
        )
        
    def fechar_playlist(self):        
        self.content = self.grid
        self.update()

        PlaylistState.close_playlist()