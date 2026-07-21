# import de interface
from ui.others.colors import color

# import de back-end
from core.services.controllers.estado_section import StateSection

# import geral
import flet as ft


class InformationMenu(ft.Container):
    def __init__(self, alter_view, page: ft.Page):
        super().__init__(
            height = 60,
            bgcolor = color.preto6,
            padding = ft.padding.all(5),
            border_radius= ft.border_radius.all(15),
            margin = ft.margin.symmetric(vertical = 5, horizontal = 10) 
        )
        self.page = page

        self.buttons = {}

        self.content = ft.Row(
            col = 6,
            alignment = ft.MainAxisAlignment.CENTER,
            
            controls = [
                self._create_text_button(
                    text = 'Letra', 
                    view = 'letra', 
                    callback = alter_view
                ),
                self._create_text_button(
                    text = 'Traduções da Letra', 
                    view = 'traducao', 
                    callback = alter_view
                )
            ]
        )

    def _create_text_button(self, text, view, callback):
        button = ft.TextButton(
            text = text,
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

        self.buttons[view] = button
        return button
    
    def did_mount(self):
        StateSection.register(
            key = 'view', 
            callback = self._when_alter_view
        )

    def will_unmount(self):
        StateSection.remove(
            key = 'view', 
            callback = self._when_alter_view
        )

    def _when_alter_view(self, view: str):
        for key, button in self.buttons.items():
            if key == view:
                button.style.bgcolor = {
                    ft.ControlState.DEFAULT: color.amarelo3,
                    ft.ControlState.HOVERED: color.amarelo,
                }
                button.style.color = color.preto1
            else:
                button.style.bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED: color.preto4,
                }
                button.style.color = color.branco
        
        self.update()