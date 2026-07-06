from ..Others.cores import cor
import flet as ft

class ContainerLoading(ft.Container):
    def __init__(self):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            bgcolor = cor.preto9,
            
            content = ft.ProgressRing(
                width = 50,
                height = 50,
                color = cor.amarelo
            )
        )