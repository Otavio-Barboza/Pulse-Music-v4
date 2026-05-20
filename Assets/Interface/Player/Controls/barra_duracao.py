from ....App.Audio.Controller.sessao import SessaoReproducao
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

        SessaoReproducao.registrar_callback(
            evento = 'posicao_slider', 
            callback = self._att_dur_atual
        )
        SessaoReproducao.registrar_callback(
            evento = 'slider', 
            callback = self._att_slider
        )
        SessaoReproducao.registrar_callback(
            evento = 'tempo_total',
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
        self.slider.max = SessaoReproducao.estado.duracao_total
        self.slider.min = 0
        self.slider.value = SessaoReproducao.estado.tempo_atual
        self.slider.update()
    
    def _att_dur_total(self, dados = None):
        self.duracao_total.value = SessaoReproducao.formatar_tempo_total()
        self.update()

    def _att_dur_atual(self, dados = None):
        self.duracao_atual.value = SessaoReproducao.formatar_tempo_atual() if SessaoReproducao.estado.tempo_atual != 0.0 else '00:00'
        
        if (
            SessaoReproducao.estado.tempo_atual > 0 
             and
            SessaoReproducao.estado.duracao_total != 0.0
        ):
            self.slider.value = min(SessaoReproducao.estado.tempo_atual, SessaoReproducao.estado.duracao_total)

        self.update()

    def detectar_arrasto_slider(self, e):
        SessaoReproducao.usuario_arrastando = True
    
    def mudar_pos_slider(self, e):
        SessaoReproducao.ir_para(e.control.value)
        SessaoReproducao.usuario_arrastando = False