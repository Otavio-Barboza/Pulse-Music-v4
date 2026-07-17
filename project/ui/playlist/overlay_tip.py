# imports de interface
from ui.others.colors import color
from ui.playlist.overlay import ContainerOverlay

# imports de back-end
from core.services.controllers.state_app import StateApp

# import geral
import flet as ft


class OverlayTip(ft.Container):
    def __init__(self, state, content_tips, mode, page: ft.Page):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            bgcolor = ft.Colors.with_opacity(0.9, color.preto3)
        )

        self.state = state
        self.content_tips = content_tips
        self.mode = mode
        self.page = page

        self.fechar = self._icon_button('Fechar')
        self.ok = self._text_button('Não mostrar novamente')
        
        self.content = ft.Container(
            height = 450,
            width = 450,
            bgcolor = color.preto8,
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
                color = color.branco,
                padding = ft.padding.all(10),
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color.laranja2
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2, color.branco)
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
                    ft.ControlState.DEFAULT : color.branco2,
                    ft.ControlState.HOVERED : color.vermelho
                },
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color.branco2
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2.5, color.vermelho)
                },
                padding = 0
            )
        )
    
    def _parar(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                state = self.state,
                mode = self.mode
            )
        )
        self.page.update()
        
        StateApp.notify(event = 'overlay_tips', data = False)
        StateApp.notify(event = 'actualization_on_click', data = False)
        StateApp.notify(event = 'actualization_switch', data = False)
    
    def _fechar(self, e):
        self.page.overlay.clear()
        self.page.overlay.append(
            ContainerOverlay(
                page = self.page,
                state = self.state,
                mode = self.mode
            )
        )
        self.page.update()