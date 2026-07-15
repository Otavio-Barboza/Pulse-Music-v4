# import de interface
from ui.others.colors import color

# import de back-end
from core.song.controller.reproduction_manager import ReproductionManager
from core.services.controllers.resize_manager import ResizeManager

# import geral
import flet as ft


class CompactProgressBar(ft.Container):
    def __init__(self):
        super().__init__(
            alignment = ft.alignment.center
        )

        self.slider = ft.Slider(
            col = {'md' : 9, 'sm' : 8.5, 'xs' : 12},
            thumb_color = color.amarelo,
            inactive_color = color.preto8,
            active_color = color.amarelo,
            overlay_color = color.amarelo_opaco2,
            on_change_end = self.mudar_pos_slider,
            on_change_start = self.detectar_arrasto_slider
        )
        self.duracao_atual = self._retornar_texto('00:00')
        self.duracao_total = self._retornar_texto('00:00')

        self.content = ft.ResponsiveRow(
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 0,

            controls = [
                self.duracao_atual,
                self.slider,
                self.duracao_total
            ]
        )

        ResizeManager.register(self._on_resize)

        ReproductionManager.register_callback(
            event = 'slider_position', 
            callback = self._att_dur_atual
        )
        ReproductionManager.register_callback(
            event = 'slider', 
            callback = self._att_slider
        )
        ReproductionManager.register_callback(
            event = 'total_time',
            callback = self._att_dur_total
        )

    def did_mount(self):
        self._on_resize()

    def _on_resize(self, e = None):
        self.duracao_atual.visible = not self.page.width < 576
        self.duracao_total.visible = not self.page.width < 576
        self.update()

    def _retornar_texto(self, texto : str) -> ft.Text:
        return ft.Text(
            value = texto,
            visible = True,
            col = {'md' : 1, 'sm' : 1.5},
            text_align = ft.TextAlign.CENTER
        )

    def _att_slider(self, dados = None):
        self.slider.max = ReproductionManager.estado.duracao_total
        self.slider.min = 0
        self.slider.value = ReproductionManager.estado.tempo_atual
        self.slider.update()
    
    def _att_dur_total(self, dados = None):
        self.duracao_total.value = ReproductionManager.formatted_total_duration()
        self.update()

    def _att_dur_atual(self, dados = None):
        self.duracao_atual.value = ReproductionManager.formatted_current_duration() if ReproductionManager.estado.tempo_atual != 0.0 else '00:00'
        
        if (
            ReproductionManager.estado.tempo_atual > 0 
             and
            ReproductionManager.estado.duracao_total != 0.0
        ):
            self.slider.value = min(ReproductionManager.estado.tempo_atual, ReproductionManager.estado.duracao_total)

        self.update()

    def detectar_arrasto_slider(self, e):
        ReproductionManager.set_drag_slider(True)
    
    def mudar_pos_slider(self, e):
        ReproductionManager.go_to(e.control.value)
        ReproductionManager.set_drag_slider(False)