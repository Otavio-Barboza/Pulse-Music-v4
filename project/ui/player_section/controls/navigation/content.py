# import geral
import flet as ft


class ContentInformation(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            content = ft.Column(
                scroll = ft.ScrollMode.AUTO,
                controls = []
            )
        )
        self.page = page

    def to_replace(self, new):
        self.content.controls.clear()
        self.content.controls.append(new)
        
        if self.page:
            self.update()