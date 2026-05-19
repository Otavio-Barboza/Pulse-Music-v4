from ....App.Audio.Controller.sessao import EstadoMusica
from ....App.Playlists.Controller.estado_playlist import EstadoPlay, PlaylistCarregada
from ..Containers.container_musica import RowContainer
from ...Others.cores import cor
import flet as ft

class ListViewMusicas(ft.ListView):
    def __init__(self, page, musicas : list | None, pasta_musicas : str):
        super().__init__(
            spacing = 10,
            expand = True
        )  
        self.page = page
        self.musicas = musicas
        self.pasta_das_musicas = pasta_musicas
        self.musicas_ids = []

        self.controls = []
        
        self._callback = self.att_container
        self._callback_qtde = self.recarregar
        self._carregar()
        
        EstadoMusica.registrar_callback(
            evento = 'att_container', 
            callback = self.att_container
        )
        EstadoPlay.registar_callback(
            evento = 'att_musicas_exibidas',
            funcao = self.recarregar
        )

    def will_unmount(self):
        EstadoMusica._callbacks['att_container'].remove(self._callback)
        EstadoPlay._callbacks['att_musicas_exibidas'].remove(self._callback_qtde)
        
    def _carregar(self):
        from ....App.Meta.Repository.tarefas import GerenciaMetadados
        import os

        if self.musicas is None:
            return
        for musica in self.musicas:
            id_musica = GerenciaMetadados.gerar_track_id(
                os.path.normpath(
                    os.path.join(
                        self.pasta_das_musicas, musica.nome + '.mp3'
                    )
                )
            )
            container = RowContainer(
                page = self.page,
                musica = musica,
                id_musica = id_musica
            )

            self.controls.append(container)
            self.musicas_ids.append(id_musica)
    
    def recarregar(self, _):
        if (
            isinstance(EstadoPlay._playlist_aberta, dict) and
            EstadoPlay._playlist_aberta['aberta'] == PlaylistCarregada.ABERTA
        ):
            try:
                self._carregar()
            except Exception as e:
                print(f'CALLBACK RECARREGA PLATLIST ERROR: {e}')

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