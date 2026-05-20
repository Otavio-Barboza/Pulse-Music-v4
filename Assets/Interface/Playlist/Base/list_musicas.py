from ....App.Audio.Controller.sessao import SessaoReproducao
from ....App.Audio.Model.modo_reproducao import Reprodução
from ....App.Playlists.Controller.estado_playlist import EstadoPlay, PlaylistCarregada
from ..Containers.container_musica import RowContainer
from ...Others.cores import cor
from ....App.Audio.Model.musica import Musica
import flet as ft

class ListViewMusicas(ft.ListView):
    def __init__(self, page, musicas : list[Musica], pasta_musicas : str | None = None):
        super().__init__(
            spacing = 10,
            expand = True
        )  
        self.page = page
        self.musicas = musicas

        self.controls = []
        
        self._callback = self.att_container
        self._callback_qtde = self.recarregar
        self._carregar()
        
        SessaoReproducao.registrar_callback(
            evento = 'att_container', 
            callback = self.att_container
        )
        EstadoPlay.registar_callback(
            evento = 'att_musicas_exibidas',
            funcao = self.recarregar
        )

    def will_unmount(self):
        SessaoReproducao._callbacks['att_container'].remove(self._callback)
        EstadoPlay._callbacks['att_musicas_exibidas'].remove(self._callback_qtde)
        
    def _carregar(self):
        if self.musicas is None:
            return
        
        for musica in self.musicas:
            container = RowContainer(
                page = self.page,
                musica = musica
            )
            
            self.controls.append(container)
    
    def recarregar(self, _):
        if (
            isinstance(EstadoPlay._playlist_aberta, dict) and
            EstadoPlay._playlist_aberta['aberta'] == PlaylistCarregada.ABERTA
        ):
            try:
                self._carregar()
            except Exception as e:
                print(f'CALLBACK RECARREGA PLATLIST ERROR: {e}')

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