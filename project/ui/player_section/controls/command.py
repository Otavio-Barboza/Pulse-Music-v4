# import de interface
from project.ui.others.colors import color

# import de back-end
from project.core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class PlayerCommands(ft.Container):
    def __init__(self, expandir, player):
        super().__init__(
            col = {'sm' : 12, 'md' : 4},
            alignment = ft.alignment.center
        )

        self.expandir = expandir
        self.player = player

        self.slider_volume_overlay = ft.Slider(
            thumb_color = color.amarelo,
            inactive_color = color.preto8,
            active_color = color.amarelo,
            overlay_color = color.amarelo_opaco2,
            value = 100,
            max = 100,
            min = 0,
            on_change = lambda e: ReproductionManager.set_volume(e.control.value / 100)
        )
        self.slider_volume = ft.Slider(
            thumb_color = color.amarelo,
            inactive_color = color.preto8,
            active_color = color.amarelo,
            overlay_color = color.amarelo_opaco2,
            value = 100,
            max = 100,
            min = 0,
            on_change = lambda e: ReproductionManager.set_volume(e.control.value / 100)
        )
        
        self.volume_overlay = ft.Container(
            expand = True,
            visible = False,
            alignment = ft.alignment.center_right,
            on_click = self._fechar_volume,
            margin = ft.margin.only(right = 30, top = 340),
            
            content = ft.Container(
                bgcolor = color.preto6,
                padding = 10,
                border_radius = 8,
                width = 300,
                height = 100,
                alignment = ft.alignment.center,
                content = self.slider_volume_overlay
            )
        )
        self.player.registrar_overlay(self.volume_overlay)
        
        self.volume = ft.Container(
            col = 8,
            visible = False,
            content = self.slider_volume
        )
        
        self.icon_volume = ft.IconButton(
            col = 6,
            icon = self.definir_volume(1.0),
            on_click = self._abrir_volume,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color.amarelo
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : color.preto1
                },
                icon_size = 25
            )
        )
        
        self.icon_expandir = ft.IconButton(
            col = 6,
            icon = ft.Icons.FULLSCREEN,
            on_click = self.expandir,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color.amarelo
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : color.preto_puro_5
                },
                icon_size = 25
            )
        )

        self.content = ft.ResponsiveRow(
            vertical_alignment = ft.CrossAxisAlignment.CENTER,

            controls = [
                self.volume, self.icon_volume, self.icon_expandir       
            ]
        )

        ReproductionManager.register_callback('volume', self.att_volume)

    def _abrir_volume(self, e):
        if not self.player.expandido.visible:
            if self.volume_overlay.visible:
                self.volume_overlay.visible = False
            else:
                self.player.fechar_overlay()
                self.volume_overlay.visible = True
        elif self.player.expandido.visible and not self.volume.visible:
            self.icon_expandir.col = 2
            self.icon_volume.col = 2
        elif self.player.expandido.visible and self.volume.visible:
            self.icon_expandir.col = 6
            self.icon_volume.col = 6
        
        self.volume.visible = not self.volume.visible if self.player.expandido.visible else False
        self.page.update()
    
    def _fechar_volume(self, e):
        self.player.fechar_overlay()
        self.page.update()
    
    def definir_volume(self, volume : float) -> ft.Icons:
        if volume >= 0.75:
            return ft.Icons.VOLUME_UP_ROUNDED
        elif 0.75 > volume >= 0.45:
            return ft.Icons.VOLUME_DOWN_ROUNDED
        elif 0.45 > volume > 0.0:
            return ft.Icons.VOLUME_MUTE_ROUNDED
        elif volume == 0.0:
            return ft.Icons.VOLUME_OFF_ROUNDED
    
    def att_volume(self, dados = None):
        self.slider_volume.value  = ReproductionManager.state.volume * 100
        self.slider_volume_overlay.value  = ReproductionManager.state.volume * 100
        self.icon_volume.icon = self.definir_volume(ReproductionManager.state.volume)
        self.update()