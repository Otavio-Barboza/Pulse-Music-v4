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


    @classmethod
    def connection_app_bar(cls, value: bool, page: ft.Page):

        # if page.appbar.connection_button.visible != value:

        if value:
            page.appbar.actions.insert(
                0, page.appbar.connection_button
            )
            page.update()
        else:
            button_to_remove = None

            for button in page.appbar.actions:
                if button.data == "connection":
                    button_to_remove = button
                    break

            if button_to_remove is not None:
                page.appbar.actions.remove(button_to_remove)

            page.update()
        # else:
        #     return