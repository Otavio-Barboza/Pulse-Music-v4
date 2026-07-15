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
    def __init__(self, musicas : list[Song], modo_favorita : ReproductionMode | None = None):
        super().__init__(
            spacing = 10,
            expand = True
        )  

        self.musicas = musicas
        self.modo_favorita = modo_favorita

        self.controls = []
        
        self._callback = self.att_container
        self._callback_qtde = self.recarregar
        self._callback_favoritas = self.att_nao_favoritas
        self._callback_favorita = self.att_favoritas
        self._carregar()
        
        ReproductionManager.register_callback(
            event = 'actualization_container', 
            callback = self.att_container
        )
        PlaylistState.register_callback(
            event = 'update_displayed_musics',
            function = self.recarregar
        )
        PlaylistState.register_callback(
            event = 'actualization_not_favorited',
            function = self.att_nao_favoritas
        )
        PlaylistState.register_callback(
            event = 'actualization_favorited',
            function = self.att_favoritas
        )

        if self.modo_favorita is not None:            
            self._callback_favoritar = self.adicionar_favorita
            self._callback_desfavoritar = self.remover_favorita

            FavoriteState.register_callback(
                event = 'add_to_favorites',
                callback = self.adicionar_favorita
            )
            FavoriteState.register_callback(
                event = 'unfavorite',
                callback = self.remover_favorita
            )

    def will_unmount(self):        
        ReproductionManager._callbacks['actualization_container'].remove(self._callback)
        PlaylistState._callbacks['update_displayed_musics'].remove(self._callback_qtde)
        PlaylistState._callbacks['actualization_not_favorited'].remove(self._callback_favoritas)
        PlaylistState._callbacks['actualization_favorited'].remove(self._callback_favorita)
        
        if self.modo_favorita is not None:
            FavoriteState._callbacks['add_to_favorites'].remove(self._callback_favoritar)
            FavoriteState._callbacks['unfavorite'].remove(self._callback_desfavoritar)
    
    def _carregar(self):        
        if self.musicas is None:
            return
        
        chaves_favoritas = FavoriteState.list_favorite()

        for musica in self.musicas:

            if musica.chave in chaves_favoritas:
                status = Favorited.FAVORITED
            else:
                status = Favorited.NOT_FAVORITED
            
            container = RowContainer(
                page = self.page,
                musica = musica,
                status_favoritada = status
            )
            
            self.controls.append(container)
            
    def recarregar(self, pasta):        
        if (
            isinstance(PlaylistState._playlist_aberta, dict) and
            PlaylistState._playlist_aberta['open_or_close'] == PlaylistLoaded.OPEN
        ):
            try:                
                if self.modo_favorita is None:
                    fonte = PlaylistFont(
                        path = pasta,
                        mode = ReproductionMode.PLAYLIST
                    )

                    self.musicas = fonte.carregar()
                    fonte.carregar_playlist(self.musicas)

                ReproductionManager.atualizar_filas_scanner()

                self.controls.clear()
                self._carregar()
                self.update()
            except Exception as e:
                print(f'CALLBACK RECARREGA PLATLIST ERROR: {e}')

    def adicionar_favorita(self, data):
        if self.modo_favorita is None:
            return
        
        self.controls.append(
            RowContainer(
                page = self.page,
                musica = data,
                status_favoritada = data.modo
            )
        )
        self.update()

        PlaylistState.notificar(
            evento = 'actualization_favorited',
            dados = data.chave
        )
    
    def remover_favorita(self, data):
        container_para_remover = None
        
        for container in self.controls:
            if container.data.chave == data.chave:
                container_para_remover = container

        self.controls.remove(container_para_remover)
        self.update()

        PlaylistState.notificar(
            'att_favoritadas',
            data.chave
        )

    def att_nao_favoritas(self, chave):
        for container in self.controls:
            if container.data.chave == chave:
                container.att_icon()
                break

    def att_favoritas(self, chave):
        for container in self.controls:
            if container.data.chave == chave:
                container.att_icon_favoritado()
                break

    def att_container(self, sessao : ReproductionManager):
        if not self.page:
            return
        
        for container in self.controls:
            if not container.page:
                continue

            if (
                sessao.estado.musica_atual is not None and
                container.data.chave is not None and
                container.data.chave == sessao.estado.musica_atual.chave
            ):
                container.bgcolor = color.amarelo3
            else:
                container.bgcolor = color.preto9

            container.update()