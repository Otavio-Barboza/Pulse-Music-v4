from Assets.Interface.Others.cores import cor
from Assets.App.Letras.Controller.letras_services import LetrasServices 
import flet as ft

class ContainerLetra(ft.Container):
    def __init__(self):
        super().__init__(
            bgcolor = cor.rosa
        )

        self.content = ft.Column(
            controls = [
                ft.Text(
                    value = self.carregar_letra()
                )
            ]
        )

    def carregar_letra(self) -> str:
        from Assets.App.Letras.Cache.memoria_letras import LetrasMemoria
        return LetrasMemoria.retornar_letra()