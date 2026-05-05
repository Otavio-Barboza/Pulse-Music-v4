from Assets.Interface.Others.cores import cor
import flet as ft

class ContainerLetra(ft.Container):
    def __init__(self):
        super().__init__(
            bgcolor = cor.rosa
        )

        self.content = ft.Column(
            controls = [
                ft.Text(
                    value = 'Letra não encotrada'
                ) for _ in range(50)
            ]
        )