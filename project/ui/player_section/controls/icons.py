# import de interface
from ui.others.colors import color

# import de back-end
from core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class PlayerIcons(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            col = {'sm' : 12, 'md' : 4},
            alignment = ft.alignment.center
        )
        self.page = page

        self.shuffle = self._create_icons(
            icon_name = ft.Icons.SHUFFLE_ROUNDED,
            backgroud_color = color.azul_medio,
            icon_color = color.branco,
            on_click = self.toggle_shuffle
        )

        self.play = self._create_icons(
            icon_name = ft.Icons.PAUSE if ReproductionManager.state.is_playing else ft.Icons.PLAY_CIRCLE_FILL_ROUNDED,
            # border_color = color.branco,
            icon_color = color.amarelo,
            backgroud_color = color.preto2,
            size = 32,
            on_click = self.toggle_play
        )

        self.repeat = self._create_icons(
            icon_name = ft.Icons.REPEAT_ROUNDED,
            backgroud_color = color.azul_medio,
            on_click = self.toggle_repeat
        )

        self.content = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                self.shuffle,
                self._create_icons(
                    icon_name = ft.Icons.SKIP_PREVIOUS_ROUNDED,
                    # border_color = color.branco,
                    icon_color = color.amarelo,
                    backgroud_color = color.preto2,
                    size = 27.5,
                    on_click = self.previous
                ),
                self.play,
                self._create_icons(
                    icon_name = ft.Icons.SKIP_NEXT_ROUNDED,
                    # border_color = color.branco,
                    icon_color = color.amarelo,
                    backgroud_color = color.preto2, 
                    size = 27.5,
                    on_click = self.next
                ),
                self.repeat
            ]
        )

        ReproductionManager.register_callback('play/pause', self.actualization_play_pause)
        ReproductionManager.register_callback('repeat', self.actualization_repeat)
        ReproductionManager.register_callback('shuffle', self.actualization_shuffle)
    
    def _create_icons(
            self, 
            icon_name: ft.Icons, 
            backgroud_color: str = color.laranja2, 
            icon_color: str = color.branco,
            border_color: str | ft.Colors = ft.Colors.TRANSPARENT,
            size: int | float = 25,
            on_click = None
        ) -> ft.IconButton:
        return ft.IconButton(
            icon = icon_name,
            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : backgroud_color
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2, border_color)
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : icon_color
                },
                icon_size = size
            ),
            on_click = on_click
        )

    def actualization_play_pause(self, *_):
        self.play.icon = ft.Icons.PAUSE if ReproductionManager.state.is_playing else ft.Icons.PLAY_CIRCLE_FILL_ROUNDED
        self.play.update()

    def actualization_repeat(self, *_):
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

    def actualization_shuffle(self, dados = None):
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

    def toggle_play(self, e):
        ReproductionManager.toggle_play_pause()
    
    def toggle_repeat(self, e):
        ReproductionManager.toggle_repeat()

    def toggle_shuffle(self, e):
        ReproductionManager.toggle_shuffle()
    
    def next(self, e):
        ReproductionManager.next()
    
    def previous(self, e):
        ReproductionManager.previous()