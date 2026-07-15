# import de front-end
from ui.others.colors import color

# import geral
import flet as ft


class ContainerLoading(ft.Container):
    def __init__(self):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            bgcolor = color.preto9,
            
            content = ft.ProgressRing(
                width = 50,
                height = 50,
                color = color.amarelo
            )
        )