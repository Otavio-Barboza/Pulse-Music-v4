# import de interface
from ui.others.colors import color

# import geral
import flet as ft


class UtilsUi:

    @classmethod
    def snack_bar(cls, text: str, page: ft.Page):
        page.open(
            ft.SnackBar(
                bgcolor = color.cinza2,

                content = ft.Text(
                    value = text,
                    size = 18,
                    weight = ft.FontWeight.BOLD,
                    color = color.preto_puro
                )
            )
        )
        page.update()