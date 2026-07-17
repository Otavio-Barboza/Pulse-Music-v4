# imports de interface
from ui.others.colors import color
from ui.playlist.content_playlist import ContentPlaylist
from ui.playlist.overlay import ContainerOverlay
from ui.playlist.overlay_tip import OverlayTip

# imports de back-end
from core.playlists.controller.playlist_manager import PlaylistManager
from core.playlists.enum.playlist_enum import PlaylistMode, PlalistOverlayMode
from core.services.settings.service_settings import ServiceSettings
from core.services.controllers.state_app import StateApp

# import geral
import flet as ft


class ColumnCards(ft.Column):
    def __init__(self, page):
        super().__init__(
            spacing = 0
        )
        self.page = page
        self.column_content = None
        self.state = None
        self.button_add_play = None
        self.button_return_play = None
        self.controls = []


    # FUNÇÕES PARA CRIAÇÃO DOS COMPONENTES
    def _create_components(self):
        self.column_content = ContentPlaylist(open_function = self.open_function)

        self.state = PlaylistManager(grid = self.column_content.grid)
 
        self.button_add_play = ft.TextButton(
            col = 4,
            text = 'Adicionar Nova Playlist',
            icon = ft.Icons.PLAYLIST_ADD,
            on_click = self._abrir_overlay_dica if ServiceSettings.load_overlay() else self._criar_overlay,
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

        self.button_return_play = ft.TextButton(
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

    def _build_class(self):
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
                        self.button_return_play
                    ]
                )
            ),
            self.column_content
        ]


    # FUNÇÃO DE CARREGAMENTO DO COMPONENTES
    def load(self):
        self._create_components()
        self._build_class()
        # self.update()

    def connect(self):
        StateApp.register_callback(event = "overlay_tips", func = ServiceSettings.save_overlay_tips)
        StateApp.register_callback("actualization_on_click", self.mudar_on_click)
    

    # FUNÇÕES DA OPERAÇÃO DA CLASSE
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
                state = self.state,
                content_tips = self.column_content,
                mode = PlalistOverlayMode.CREATE
            )
        )
        self.page.update()

    def _criar_overlay(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                state = self.state,
                mode = PlalistOverlayMode.CREATE
            )
        )
        self.page.update()
    
    def update_buttons(self):
        if self.state.mode == PlaylistMode.GRID:
            self.button_add_play.visible = True
            self.button_return_play.visible = False
        elif self.state.mode == PlaylistMode.LIST:
            self.button_add_play.visible = False
            self.button_return_play.visible = True

        self.update()

    def carregar(self):
        """
            Intermedio ao ContentPlaylist para o carregamento dos cards ao inicializar o player
        """
        self.update_buttons()
        self.column_content.carregar()
    
    def open_function(self):
        self.state.modo = PlaylistMode.LIST
        self.update_buttons()

    def voltar(self, e):
        self.state.modo = PlaylistMode.GRID
        self.update_buttons()
        self.column_content.fechar_playlist()
        self.column_content.carregar()