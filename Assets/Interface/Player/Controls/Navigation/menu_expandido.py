from Assets.Interface.Others.cores import cor
from Assets.App.Services.Controllers.estado_section import EstadoSection
import flet as ft

class MenuInfos(ft.Container):
    def __init__(self, page, trocar_view):
        super().__init__(
            height = 60,
            bgcolor = cor.preto6,
            padding = ft.padding.all(5),
            border_radius= ft.border_radius.all(15),
            margin = ft.margin.symmetric(vertical = 5, horizontal = 10) 
        )
        self.page = page
        self.botoes = {}

        self.content = ft.Row(
            col = 6,
            alignment = ft.MainAxisAlignment.CENTER,
            
            controls = [
                self._botao(texto = 'Informações', view = 'info', callback = trocar_view),
                self._botao(texto = 'Letra', view = 'letra', callback = trocar_view),
                self._botao(texto = 'Artista', view = 'artista', callback = trocar_view)
            ]
        )

    def _botao(self, texto, view, callback):
        botao = ft.TextButton(
            text = texto,
            on_click = lambda e: callback(view),
            width = 100,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : cor.amarelo
                },
                color = {
                    ft.ControlState.DEFAULT : cor.branco3,
                    ft.ControlState.HOVERED : cor.preto3
                },
                shape = ft.RoundedRectangleBorder(radius = 5),
                alignment = ft.alignment.center
            )
        )

        self.botoes[view] = botao
        return botao
    
    def did_mount(self):
        EstadoSection.registrar('view', self._quando_view_mudar)

    def will_unmount(self):
        EstadoSection.remover('view', self._quando_view_mudar)

    def _quando_view_mudar(self, view : str):
        for chave, botao in self.botoes.items():
            if chave == view:
                botao.style.bgcolor = {
                    ft.ControlState.DEFAULT: cor.amarelo3,
                    ft.ControlState.HOVERED: cor.amarelo,
                }
                botao.style.color = cor.preto1
            else:
                botao.style.bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED: cor.preto4,
                }
                botao.style.color = cor.branco
        
        self.update()