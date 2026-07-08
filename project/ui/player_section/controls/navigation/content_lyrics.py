# import de interface
from project.ui.others.colors import color

# import de back-end
from Assets.App.Letras.Controller.letras_services import LetrasServices 

# import geral
import flet as ft


class LyricsContainer(ft.Container):
    def __init__(self):
        super().__init__(
            padding = ft.padding.only(right = 30, left = 10),
            margin = ft.margin.only(bottom = 10),
            expand = True,
            alignment = ft.alignment.center
        )

        self.content = ft.Column(
            controls = [
                ft.Text(
                    value = self.carregar_letra(),
                    size = 18,
                    weight = ft.FontWeight.W_500
                )
            ]
        )

        self.callback = self.atualizar_letra
        LetrasServices.registrar_callback(
            evento = 'att_letra',
            callback = self.atualizar_letra
        )

    def did_mount(self):
        LetrasServices.set_tela_expandida(True)

    def will_unmount(self):
        LetrasServices.set_tela_expandida(False)
        
        if self.callback in LetrasServices._callbacks['att_letra']:
            LetrasServices._callbacks['att_letra'].remove(self.callback)
        
    def carregar_letra(self) -> str:
        from Assets.App.Letras.Cache.memoria_letras import LetrasMemoria
        return LetrasMemoria.retornar_letra()
    
    def atualizar_letra(self, *_):
        self.content.controls[0].value = self.carregar_letra()
        self.update()