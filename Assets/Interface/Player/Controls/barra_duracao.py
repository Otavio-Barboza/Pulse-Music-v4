from ....App.Audio.Controller.estado_musica import EstadoMusica
from ....App.Services.Controllers.estado_redimensionamento import ResizeManager
from ...Others.cores import cor
import flet as ft
import asyncio

class BarraDuracaoCompacta(ft.Container):
    def __init__(self, page):
        super().__init__(
            alignment = ft.alignment.center
        )

        self.page = page

        self.slider = ft.Slider(
            col = {'md' : 9, 'sm' : 8.5, 'xs' : 12},
            thumb_color = cor.amarelo,
            inactive_color = cor.preto8,
            active_color = cor.amarelo,
            overlay_color = cor.amarelo_opaco2,
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

        ResizeManager.registrar(self._on_resize)
        EstadoMusica.registrar_callback(evento='texto_barra_duracao', callback=self._att_dur_total)
        EstadoMusica.registrar_callback(evento='tempo', callback=self._att_dur_atual)
        EstadoMusica.registrar_callback(evento='texto_barra_duracao', callback=self._att_slider)

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

    def _att_slider(self, estado : EstadoMusica):
        self.slider.max = estado.duracao_total
        self.slider.min = 0
        self.slider.value = estado.tempo_atual
        self.slider.update()
    
    def _att_dur_total(self, estado : EstadoMusica):
        self.duracao_total.value = estado._tempo_total_formatado
        self.update()

    def _att_dur_atual(self, estado : EstadoMusica):
        self.duracao_atual.value = estado._tempo_atual_formatado if estado.tempo_atual != 0.0 else '00:00'
        
        if estado.tempo_atual > 0:
            self.slider.value = min(estado.tempo_atual, estado.duracao_total + 0.01)

        self.update()

    def detectar_arrasto_slider(self, e):
        EstadoMusica.usuario_arrastando = True
    
    def mudar_pos_slider(self, e):
        EstadoMusica.ir_para(e.control.value)
        EstadoMusica.usuario_arrastando = False