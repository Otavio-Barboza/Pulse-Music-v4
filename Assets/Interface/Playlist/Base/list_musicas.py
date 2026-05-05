from ....App.Audio.Controller.estado_musica import EstadoMusica
from ..Containers.container_musica import RowContainer
from ...Others.cores import cor
import flet as ft

class ListViewMusicas(ft.ListView):
    def __init__(self, page, musicas : list | None, tipagem : str):
        super().__init__(
            spacing = 10,
            expand = True
        )  
        self.page = page
        self.musicas = musicas
        self.tipagem = tipagem
        self.controls = []
        self._callback = self.att_container
        self._carregar()
        EstadoMusica.registrar_callback('att_container', self.att_container)

    def will_unmount(self):
        EstadoMusica._callbacks['att_container'].remove(self._callback)
        
    def _carregar(self):
        if self.musicas is None:
            return
        for musica in self.musicas:
            container = RowContainer(
                page = self.page,
                musica = musica,
                tipagem = 'play'
            )
            self.controls.append(container)

    def att_container(self, estado : EstadoMusica):
        if not self.page:
            return
        
        for container in self.controls:
            if not container.page:
                continue

            if estado.musica_atual and container.data.id == estado.musica_atual.id:
                container.bgcolor = cor.amarelo3
            else:
                container.bgcolor = cor.preto9

            container.update()