from ....App.Audio.Controller.sessao import SessaoReproducao
from ....App.Audio.Model.modo_reproducao import Reprodução
from ....App.Playlists.Controller.estado_playlist import EstadoPlay, PlaylistCarregada
from ..Containers.container_musica import RowContainer
from ...Others.cores import cor
from ....App.Audio.Model.musica import Musica
import flet as ft

class ListViewMusicas(ft.ListView):
    def __init__(self, page, musicas : list[Musica], modo_favorita : str | None = None):
        super().__init__(
            spacing = 10,
            expand = True
        )  
        self.page = page
        self.musicas = musicas
        self.modo_favorita = modo_favorita

        self.controls = []
        
        self._callback = self.att_container
        self._callback_qtde = self.recarregar
        self._callback_favoritas = self.att_nao_favoritas
        self._callback_favorita = self.att_favoritas
        self._carregar()
        
        SessaoReproducao.registrar_callback(
            evento = 'att_container', 
            callback = self.att_container
        )
        EstadoPlay.registar_callback(
            evento = 'att_musicas_exibidas',
            funcao = self.recarregar
        )
        EstadoPlay.registar_callback(
            evento = 'att_favoritadas',
            funcao = self.att_nao_favoritas
        )
        EstadoPlay.registar_callback(
            evento = 'att_favoritada',
            funcao = self.att_favoritas
        )

        if self.modo_favorita is not None:
            from ....App.Favoritas.Controller.favoritas_controller import EstadoFavoritas
            
            self._callback_favoritar = self.adicionar_favorita
            self._callback_desfavoritar = self.remover_favorita

            EstadoFavoritas.registrar_callback(
                evento = 'favoritar',
                callback = self.adicionar_favorita
            )
            EstadoFavoritas.registrar_callback(
                evento = 'desfavoritar',
                callback = self.remover_favorita
            )

    def will_unmount(self):
        from ....App.Favoritas.Controller.favoritas_controller import EstadoFavoritas
        
        SessaoReproducao._callbacks['att_container'].remove(self._callback)
        EstadoPlay._callbacks['att_musicas_exibidas'].remove(self._callback_qtde)
        EstadoPlay._callbacks['att_favoritadas'].remove(self._callback_favoritas)
        EstadoPlay._callbacks['att_favoritada'].remove(self._callback_favorita)
        
        if self.modo_favorita is not None:
            EstadoFavoritas._callbacks['favoritar'].remove(self._callback_favoritar)
            EstadoFavoritas._callbacks['desfavoritar'].remove(self._callback_desfavoritar)
    
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
        
        if (
            isinstance(EstadoPlay._playlist_aberta, dict) and
            EstadoPlay._playlist_aberta['aberta'] == PlaylistCarregada.ABERTA
        ):
            try:                
                fonte = FontePlaylist(
                    pasta = pasta,
                    modo = ModoReprodução.PLAYLIST if self.modo_favorita is None else ModoReprodução.FAVORITA
                )

                self.musicas = None
                self.musicas = fonte.carregar()
                
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

        EstadoPlay.notificar(
            evento = 'att_favoritada',
            dados = data.chave
        )
    
    def remover_favorita(self, data):
        container_para_remover = None
        
        for container in self.controls:
            if container.data.chave == data.chave:
                container_para_remover = container

        self.controls.remove(container_para_remover)
        self.update()

        EstadoPlay.notificar(
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
                container.bgcolor = cor.amarelo3
            else:
                container.bgcolor = cor.preto9

            container.update()