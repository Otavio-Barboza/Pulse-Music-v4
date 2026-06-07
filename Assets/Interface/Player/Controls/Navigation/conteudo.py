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
        # print("ANTES", novo.parent, novo.page)

        self.content.controls.clear()
        self.content.controls.append(novo)
        
        # print("DEPOIS", novo.parent, novo.page)

        if self.page:
            self.update()

        # print("UPDATE", novo.parent, novo.page)