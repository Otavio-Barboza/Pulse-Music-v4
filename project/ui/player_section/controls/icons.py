# import de interface
from ui.others.colors import color

# import de back-end
from core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class PlayerIcons(ft.Container):
    def __init__(self):
        super().__init__(
            col = {'sm' : 12, 'md' : 4},
            alignment = ft.alignment.center
        )
        
        self.shuffle = self._criar_icons(
            nome_icon = ft.Icons.SHUFFLE_ROUNDED,
            color_fundo = color.azul_medio,
            color_icon = color.branco,
            on_click = self.toggle_aleatorio
        )

        self.tocar = self._criar_icons(
            nome_icon = ft.Icons.PAUSE if ReproductionManager.state.is_playing else ft.Icons.PLAY_CIRCLE_FILL_ROUNDED,
            # color_borda = color.branco,
            color_icon = color.amarelo,
            color_fundo = color.preto2,
            tamanho = 32,
            on_click = self.toogle_tocar
        )

        self.repeat = self._criar_icons(
            nome_icon = ft.Icons.REPEAT_ROUNDED,
            color_fundo = color.azul_medio,
            on_click = self.toggle_repetir
        )

        self.content = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                self.shuffle,
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
                self.repeat
            ]
        )

        ReproductionManager.register_callback('play/pause', self._atualizar_play_pause)
        ReproductionManager.register_callback('repeat', self.att_repetir)
        ReproductionManager.register_callback('shuffle', self.att_aleatorio)
    
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
        self.tocar.icon = ft.Icons.PAUSE if ReproductionManager.state.is_playing else ft.Icons.PLAY_CIRCLE_FILL_ROUNDED
        self.tocar.update()

    def att_repetir(self, dados = None):
        self.repeat.icon = ft.Icons.REPEAT_ONE_ON_ROUNDED if ReproductionManager.configuration.repeat else ft.Icons.REPEAT_ROUNDED

        self.repeat.style = ft.ButtonStyle(
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
        ) if not ReproductionManager.configuration.repeat else ft.ButtonStyle(
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
        self.repeat.update()

    def att_aleatorio(self, dados = None):
        self.shuffle.icon = ft.Icons.SHUFFLE_ON_ROUNDED if ReproductionManager.configuration.shuffle else ft.Icons.SHUFFLE_ROUNDED
        self.shuffle.style = ft.ButtonStyle(
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
        ) if not ReproductionManager.configuration.shuffle else ft.ButtonStyle(
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
        self.shuffle.update()

    def toogle_tocar(self, e):
        ReproductionManager.toggle_play_pause()
    
    def toggle_repetir(self, e):
        ReproductionManager.toggle_repeat()

    def toggle_aleatorio(self, e):
        ReproductionManager.toggle_shuffle()
    
    def _proximo(self, e):
        ReproductionManager.next()
    
    def _anterior(self, e):
        ReproductionManager.previous()