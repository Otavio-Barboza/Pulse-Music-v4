from ...App.Services.Config.config_service import ConfigService
from ...App.Services.Controllers.estado_app import EstadoApp
from ..Others.cores import cor
from.overlay import ContainerOverlay
import flet as ft

class OverlayDica(ft.Container):
    def __init__(self, page, estado, conteudo, modo):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            bgcolor = ft.Colors.with_opacity(0.9, cor.preto3)
        )
        self.page = page
        self.estado = estado
        self.conteudo = conteudo
        self.modo = modo

        self.fechar = self._icon_button('Fechar')
        self.ok = self._text_button('Não mostrar novamente')
        
        self.content = ft.Container(
            height = 450,
            width = 450,
            bgcolor = cor.preto8,
            alignment = ft.alignment.center,
            border_radius = ft.border_radius.all(20),
            padding = ft.padding.only(
                top = 10,
                bottom = 10,
                left = 20,
                right = 20 
            ),

            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,
                spacing = 15,
                expand = True,

                controls = [
                    self._text(
                        text = 'Bem-vindo(a)!',
                        tamanho = 30,
                        negrito = ft.FontWeight.BOLD,
                        altura = 45
                    ),
                    self._text(
                        text = 'Para garantir a melhor experiência no aplicativo:',
                        alinhamento = ft.TextAlign.START,
                        altura = 60
                    ),
                    self._text(
                        text = '• Cada playlist pode conter no máximo 1500 músicas (obrigatório).\n• Para maior fluidez, recomendamos até 1000 músicas por playlist.',
                        alinhamento = ft.TextAlign.JUSTIFY,
                        altura = 110
                    ),
                    self._text(
                        text = 'Essa limitação evita lentidão e garante uma navegação mais suave.',
                        alinhamento = ft.TextAlign.JUSTIFY,
                        altura = 60
                    ),

                    ft.Row(
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                        height = 55,

                        controls = [
                            self.fechar, self.ok
                        ]
                    ) 
                ]
            )
        )
    
    def _text(
        self, 
        text : str,
        tamanho : int = 18,
        negrito : ft.FontWeight = ft.FontWeight.W_500,
        alinhamento : ft.TextAlign = ft.TextAlign.CENTER,
        altura : int = 40
    ) -> ft.Text:
        return ft.Text(
            value = text,
            size = tamanho,
            weight = negrito,
            text_align = alinhamento,
            height = altura
        )
    
    def _text_button(self, text : str) -> ft.TextButton:
        return ft.TextButton(
            text = text,
            on_click = self._parar,
            height = 45,

            style = ft.ButtonStyle(
                color = cor.branco,
                padding = ft.padding.all(10),
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : cor.laranja2
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2, cor.branco)
                },
                text_style = ft.TextStyle(
                    size = 16,
                    weight = ft.FontWeight.W_500
                )
            )
        )
    
    def _icon_button(self, text : str) -> ft.IconButton:
        return ft.IconButton(
            icon = ft.Icons.CLOSE,
            on_click = self._fechar,

            style = ft.ButtonStyle(
                color = {
                    ft.ControlState.DEFAULT : cor.branco2,
                    ft.ControlState.HOVERED : cor.vermelho
                },
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : cor.branco2
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2.5, cor.vermelho)
                },
                padding = 0
            )
        )
    
    def _parar(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                estado = self.estado,
                conteudo = self.conteudo,
                modo = self.modo
            )
        )
        self.page.update()
        EstadoApp.notificar('overlay_dicas', dados = False)
        EstadoApp.notificar('att_on_click', dados = False)
        EstadoApp.notificar('att_switch', dados = False)
    
    def _fechar(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                estado = self.estado,
                conteudo = self.conteudo,
                modo = self.modo
            )
        )
        self.page.update()