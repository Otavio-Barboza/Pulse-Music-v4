from Assets.Interface.Others.cores import cor
import flet as ft

class ConteudoInfos(ft.Container):
    def __init__(self):
        super().__init__(
            content = ft.Column(
                scroll = ft.ScrollMode.AUTO,
                controls = []
            )
        )

    def trocar(self, novo):
        self.content.controls.clear()
        self.content.controls.append(novo)