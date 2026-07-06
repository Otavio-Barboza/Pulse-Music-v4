from project.ui.others.colors import color
from ..content_playlist import PlaylistConteudo
from ..overlay import ContainerOverlay
from project.ui.playlist.overlay_tip import OverlayTip
from ....App.Playlists.Controller.estado_playlist import EstadoPlaylist, ModoOverlayPlaylist, ModoPlaylist
from ....App.Services.Config.config_service import ConfigService
from ....App.Playlists.Repository.playlist_reprositorio import PlaylistRepositorio
from ....App.Services.Controllers.estado_app import EstadoApp
import flet as ft

class ColumnCards(ft.Column):
    def __init__(self, page):
        super().__init__(
            spacing = 0
        )
        self.page = page
        self.conteudo = PlaylistConteudo(page = self.page, abrir = self.abrir)
        self.estado = EstadoPlaylist(grid = self.conteudo.grid)

        self.button_add_play = ft.TextButton(
            col = 4,
            text = 'Adicionar Nova Playlist',
            icon = ft.Icons.PLAYLIST_ADD,
            on_click = self._abrir_overlay_dica if ConfigService.ler_overlay() else self._criar_overlay,
            visible = True,
            
            style = ft.ButtonStyle(
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : color.preto_puro
                },
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.with_opacity(0.4, color.preto_puro_5),
                    ft.ControlState.HOVERED : color.amarelo
                },
                text_style = ft.TextStyle(
                    size = 16,
                    weight = ft.FontWeight.W_500
                ),
                
                padding = ft.padding.all(15),
                shape = ft.RoundedRectangleBorder(radius = 10),
                icon_size = 20
            )
        )
        self.button_retorna_play = ft.TextButton(
            col = 4,
            text = 'Voltar',
            on_click = self.voltar,
            visible = False,

            style = ft.ButtonStyle(
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : color.preto_puro
                },
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color.amarelo
                },
                text_style = ft.TextStyle(
                    size = 16,
                    weight = ft.FontWeight.W_500
                ),
                
                padding = ft.padding.all(15),
                shape = ft.RoundedRectangleBorder(radius = 10),
            )
        )

        self.controls = [
            ft.Container(
                margin = ft.margin.only(
                    top = 10,
                    bottom = 10
                ),
                content = ft.ResponsiveRow(
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.CENTER,

                    controls = [
                        self.button_add_play,
                        self.button_retorna_play
                    ]
                )
            ),
            self.conteudo
        ]

        EstadoApp.registrar_ouvinte(evento = 'overlay_dicas', func = ConfigService.salvar_overlay_dicas)
        EstadoApp.registrar_ouvinte('att_on_click', self.mudar_on_click)

    def mudar_on_click(self, valor):
        if valor == True:
            self.button_add_play.on_click = self._abrir_overlay_dica
        else:
            self.button_add_play.on_click = self._criar_overlay
        self.update()

    def _abrir_overlay_dica(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            OverlayTip(
                page = self.page,
                estado = self.estado,
                conteudo = self.conteudo,
                modo = ModoOverlayPlaylist.CREATE
            )
        )
        self.page.update()

    def _criar_overlay(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                estado = self.estado,
                conteudo = self.conteudo,
                modo = ModoOverlayPlaylist.CREATE
            )
        )
        self.page.update()
    
    def _atualizar_botoes(self):
        if self.estado.modo == ModoPlaylist.GRID:
            self.button_add_play.visible = True
            self.button_retorna_play.visible = False
        elif self.estado.modo == ModoPlaylist.LISTA:
            self.button_add_play.visible = False
            self.button_retorna_play.visible = True

        self.update()

    def carregar(self):
        """
            Intermedio ao PlaylistConteudo para o carregamento dos cards ao inicializar o player
        """
        self._atualizar_botoes()
        self.conteudo.carregar()
    
    def abrir(self):
        self.estado.modo = ModoPlaylist.LISTA
        self._atualizar_botoes()

    def voltar(self, e):
        self.estado.modo = ModoPlaylist.GRID
        self._atualizar_botoes()
        self.conteudo.fechar_playlist()
        self.conteudo.carregar()