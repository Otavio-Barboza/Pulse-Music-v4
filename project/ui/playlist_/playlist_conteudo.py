from ...App.Playlists.Controller.estado_playlist import EstadoPlaylist, ModoOverlayPlaylist
from ...App.Audio.Controller.sessao import SessaoReproducao
from ...App.Audio.Fontes.fonte_playlist import FontePlaylist
from ...App.Playlists.Controller.estado_playlist import PlaylistCarregada
from .Base.grid_playlists import GridPlaylists
from .Base.list_musicas import ListViewMusicas
from .overlay import ContainerOverlay
from ..Others.cores import cor
import flet as ft
import os

class PlaylistConteudo(ft.Container):
    def __init__(self, page, abrir):
        super().__init__(
            padding = ft.padding.all(10),
            expand = True
        )
        self.page = page
        self.abrir = abrir

        self.grid = GridPlaylists(
            page = self.page,
            on_abrir = self.abrir_config_playlist,
            on_remover = self._remover_playlist,
            carregar_musicas = self.abrir_playlist
        )
        self.estado = EstadoPlaylist(self.grid)
        
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
                modo = ModoOverlayPlaylist.UPDATE
            ) 
        )
        self.page.update()
    
    def _remover_playlist(self, playlist_id : str):
        from ...App.Meta.Scanner.scanner import Scanner
        from ...App.Playlists.Repository.playlist_reprositorio import PlaylistRepositorio
        
        """
            Ordem: EstadoPlaylist -> Grid & Repositorio -> CreatePlaylist
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
            Ordem: EstadoPlaylist ->
        Args:
            id (str): ID da playlist
        """
        from ...App.Playlists.Controller.estado_playlist import EstadoPlay
        from ...App.Audio.Model.modo_reproducao import ModoReprodução

        card = self.grid.cards[id]

        fonte = FontePlaylist(
            pasta = card.pasta,
            modo = ModoReprodução.PLAYLIST
        )
        
        lista_de_musicas = fonte.carregar()
        
        fonte.carregar_playlist(
            lista_musicas = lista_de_musicas
        )

        self.abrir()

        list_view = ListViewMusicas(
            page = self.page,
            musicas = lista_de_musicas,
            modo_favorita = None
        )
        
        self.content = list_view
        self.update()

        EstadoPlay.abrir_playlist(
            id_playlist = card.data['id'],
            status = PlaylistCarregada.ABERTA
        )
        
    def fechar_playlist(self):
        from ...App.Playlists.Controller.estado_playlist import EstadoPlay
        
        self.content = self.grid
        self.update()

        EstadoPlay.fechar_playlist()