from ....App.Audio.Controller.sessao import SessaoReproducao
from project.ui.others.colors import color
import flet as ft

class PlayerIcons(ft.Container):
    def __init__(self):
        super().__init__(
            col = {'sm' : 12, 'md' : 4},
            alignment = ft.alignment.center
        )
        
        self.aleatorio = self._criar_icons(
            nome_icon = ft.Icons.SHUFFLE_ROUNDED,
            color_fundo = color.azul_medio,
            color_icon = color.branco,
            on_click = self.toggle_aleatorio
        )

        self.tocar = self._criar_icons(
            nome_icon = ft.Icons.PAUSE if SessaoReproducao.estado.tocando else ft.Icons.PLAY_CIRCLE_FILL_ROUNDED,
            # color_borda = color.branco,
            color_icon = color.amarelo,
            color_fundo = color.preto2,
            tamanho = 32,
            on_click = self.toogle_tocar
        )

        self.repetir = self._criar_icons(
            nome_icon = ft.Icons.REPEAT_ROUNDED,
            color_fundo = color.azul_medio,
            on_click = self.toggle_repetir
        )

        self.content = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                self.aleatorio,
                self._criar_icons(
                    nome_icon = ft.Icons.SKIP_PREVIOUS_ROUNDED,
                    # color_borda = color.branco,
                    color_icon = color.amarelo,
                    color_fundo = color.preto2,
                    tamanho = 27.5,
                    on_click = self._anterior
                ),
                self.tocar,
                self._criar_icons(
                    nome_icon = ft.Icons.SKIP_NEXT_ROUNDED,
                    # color_borda = color.branco,
                    color_icon = color.amarelo,
                    color_fundo = color.preto2, 
                    tamanho = 27.5,
                    on_click = self._proximo
                ),
                self.repetir
            ]
        )

        SessaoReproducao.registrar_callback('play/pause', self._atualizar_play_pause)
        SessaoReproducao.registrar_callback('repetir', self.att_repetir)
        SessaoReproducao.registrar_callback('aleatorio', self.att_aleatorio)
    
    def _criar_icons(
            self, 
            nome_icon : ft.Icons, 
            color_fundo : str = color.laranja2, 
            color_icon : str = color.branco,
            color_borda : str | ft.Colors = ft.Colors.TRANSPARENT,
            tamanho : int | float = 25,
            on_click = None
        ) -> ft.IconButton:
        return ft.IconButton(
            icon = nome_icon,
            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color_fundo
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2, color_borda)
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : color_icon
                },
                icon_size = tamanho
            ),
            on_click = on_click
        )

    def _atualizar_play_pause(self, dados = None):
        self.tocar.icon = ft.Icons.PAUSE if SessaoReproducao.estado.tocando else ft.Icons.PLAY_CIRCLE_FILL_ROUNDED
        self.tocar.update()

    def att_repetir(self, dados = None):
        self.repetir.icon = ft.Icons.REPEAT_ONE_ON_ROUNDED if SessaoReproducao.config.repetir else ft.Icons.REPEAT_ROUNDED

        self.repetir.style = ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                ft.ControlState.HOVERED : color.azul_medio
            },
            side = {
                ft.ControlState.HOVERED : ft.BorderSide(2, ft.Colors.TRANSPARENT)
            },
            color = {
                ft.ControlState.DEFAULT : color.branco,
                ft.ControlState.HOVERED : color.branco
            },
            icon_size = 25
        ) if not SessaoReproducao.config.repetir else ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                ft.ControlState.HOVERED : color.branco
            },
            color = {
                ft.ControlState.DEFAULT : color.azul_medio,
                ft.ControlState.HOVERED : color.azul_medio
            },
            icon_size = 25
        )
        self.repetir.update()

    def att_aleatorio(self, dados = None):
        self.aleatorio.icon = ft.Icons.SHUFFLE_ON_ROUNDED if SessaoReproducao.config.aleatorio else ft.Icons.SHUFFLE_ROUNDED
        self.aleatorio.style = ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                ft.ControlState.HOVERED : color.azul_medio
            },
            side = {
                ft.ControlState.HOVERED : ft.BorderSide(2, ft.Colors.TRANSPARENT)
            },
            color = {
                ft.ControlState.DEFAULT : color.branco,
                ft.ControlState.HOVERED : color.branco
            },
            icon_size = 25
        ) if not SessaoReproducao.config.aleatorio else ft.ButtonStyle(
            bgcolor = {
                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                ft.ControlState.HOVERED : color.branco
            },
            side = {
                ft.ControlState.HOVERED : ft.BorderSide(2, ft.Colors.TRANSPARENT)
            },
            color = {
                ft.ControlState.DEFAULT : color.branco,
                ft.ControlState.HOVERED : color.azul_medio
            },
            icon_size = 25
        )
        self.aleatorio.update()

    def toogle_tocar(self, e):
        SessaoReproducao.toggle_play_pause()
    
    def toggle_repetir(self, e):
        SessaoReproducao.toggle_repetir()

    def toggle_aleatorio(self, e):
        SessaoReproducao.toggle_aleatorio()
    
    def _proximo(self, e):
        SessaoReproducao.proxima()
    
    def _anterior(self, e):
        SessaoReproducao.anterior()