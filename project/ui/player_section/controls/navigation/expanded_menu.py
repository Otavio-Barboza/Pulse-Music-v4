# import de interface
from ui.others.colors import color

# import de back-end
from core.services.controllers.estado_section import EstadoSection

# import geral
import flet as ft


class InformationMenu(ft.Container):
    def __init__(self, trocar_view):
        super().__init__(
            height = 60,
            bgcolor = color.preto6,
            padding = ft.padding.all(5),
            border_radius= ft.border_radius.all(15),
            margin = ft.margin.symmetric(vertical = 5, horizontal = 10) 
        )

        self.botoes = {}

        self.content = ft.Row(
            col = 6,
            alignment = ft.MainAxisAlignment.CENTER,
            
            controls = [
                self._botao(texto = 'Letra', view = 'letra', callback = trocar_view),
                self._botao(texto = 'Traduções da Letra', view = 'traducao', callback = trocar_view)
            ]
        )

    def _botao(self, texto, view, callback):
        botao = ft.TextButton(
            text = texto,
            on_click = lambda e: callback(view),
            width = 150,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : color.amarelo
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco3,
                    ft.ControlState.HOVERED : color.preto3
                },
                shape = ft.RoundedRectangleBorder(radius = 5),
                alignment = ft.alignment.center
            )
        )

        self.botoes[view] = botao
        return botao
    
    def did_mount(self):
        EstadoSection.register('view', self._quando_view_mudar)

    def will_unmount(self):
        EstadoSection.remove('view', self._quando_view_mudar)

    def _quando_view_mudar(self, view : str):
        for chave, botao in self.botoes.items():
            if chave == view:
                botao.style.bgcolor = {
                    ft.ControlState.DEFAULT: color.amarelo3,
                    ft.ControlState.HOVERED: color.amarelo,
                }
                botao.style.color = color.preto1
            else:
                botao.style.bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED: color.preto4,
                }
                botao.style.color = color.branco
        
        self.update()