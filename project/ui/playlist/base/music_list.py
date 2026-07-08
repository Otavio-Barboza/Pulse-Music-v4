# import de interface
from project.ui.others.colors import color
from project.ui.playlist.containers.music_container import RowContainer

# import de back-end
from ....App.Audio.Controller.sessao import SessaoReproducao
from ....App.Audio.Model.modo_reproducao import Reprodução
from project.core.playlists.controller.estado_playlist import PlaylistState
from project.core.playlists.enum.playlist_enum import PlaylistLoaded
from project.core.song.model.song import Song

# import geral
import flet as ft

class ListViewMusic(ft.ListView):
    def __init__(self, musicas : list[Song], modo_favorita : ModoReprodução | None = None):
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
        
        SessaoReproducao.registrar_callback(
            evento = 'actualization_container', 
            callback = self.att_container
        )
        PlaylistState.registar_callback(
            evento = 'update_displayed_musics',
            funcao = self.recarregar
        )
        PlaylistState.registar_callback(
            evento = 'actualization_not_favorited',
            funcao = self.att_nao_favoritas
        )
        PlaylistState.registar_callback(
            evento = 'actualization_favorited',
            funcao = self.att_favoritas
        )

        if self.modo_favorita is not None:
            from ....App.Favoritas.Controller.favoritas_controller import EstadoFavoritas
            
            self._callback_favoritar = self.adicionar_favorita
            self._callback_desfavoritar = self.remover_favorita

            EstadoFavoritas.registrar_callback(
                evento = 'add_to_favorites',
                callback = self.adicionar_favorita
            )
            EstadoFavoritas.registrar_callback(
                evento = 'unfavorite',
                callback = self.remover_favorita
            )

    def will_unmount(self):
        from ....App.Favoritas.Controller.favoritas_controller import EstadoFavoritas
        
        SessaoReproducao._callbacks['actualization_container'].remove(self._callback)
        PlaylistState._callbacks['update_displayed_musics'].remove(self._callback_qtde)
        PlaylistState._callbacks['actualization_not_favorited'].remove(self._callback_favoritas)
        PlaylistState._callbacks['actualization_favorited'].remove(self._callback_favorita)
        
        if self.modo_favorita is not None:
            EstadoFavoritas._callbacks['add_to_favorites'].remove(self._callback_favoritar)
            EstadoFavoritas._callbacks['unfavorite'].remove(self._callback_desfavoritar)
    
    def _carregar(self):
        from ....App.Favoritas.Controller.favoritas_controller import EstadoFavoritas, Favoritada
        
        if self.musicas is None:
            return
        
        chaves_favoritas = EstadoFavoritas.listar_favoritas()

        for musica in self.musicas:

            if musica.chave in chaves_favoritas:
                status = Favoritada.FAVORITADA
            else:
                status = Favoritada.NAO_FAVORITADA
            
            container = RowContainer(
                page = self.page,
                musica = musica,
                status_favoritada = status
            )
            
            self.controls.append(container)
            
    def recarregar(self, pasta):
        from ....App.Audio.Fontes.fonte_playlist import FontePlaylist
        from ....App.Audio.Model.modo_reproducao import ModoReprodução
        # from ....App.Audio.Controller.sessao import SessaoReproducao
        
        if (
            isinstance(PlaylistState._playlist_aberta, dict) and
            PlaylistState._playlist_aberta['open_or_close'] == PlaylistLoaded.OPEN
        ):
            try:                
                if self.modo_favorita is None:
                    fonte = FontePlaylist(
                        pasta = pasta,
                        modo = ModoReprodução.PLAYLIST
                    )

                    self.musicas = fonte.carregar()
                    fonte.carregar_playlist(self.musicas)

                SessaoReproducao.atualizar_filas_scanner()

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

    def att_container(self, sessao : SessaoReproducao):
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