from Assets.App.Letras.Controller.letras_services import LetrasServices
from ....Others.cores import cor
import flet as ft

class ContainerTraducao(ft.Container):
    def __init__(self):
        super().__init__(
            padding = ft.padding.only(right = 30, left = 10),
            margin = ft.margin.only(bottom = 10),
            expand = True,
            alignment = ft.alignment.center
        )

        self.infos = ft.PopupMenuButton(
            icon = ft.Icons.G_TRANSLATE,
            icon_color = cor.preto3,
            surface_tint_color = cor.branco,
            bgcolor = cor.preto3,
            shadow_color = cor.branco,
            tooltip = "Idiomas",

            style = ft.ButtonStyle(
                color = {
                    ft.ControlState.DEFAULT : cor.azul_medio2,
                    ft.ControlState.HOVERED : cor.azul_medio
                },
                overlay_color = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.DEFAULT : cor.branco
                }
            ),

            items = [
                ft.PopupMenuItem(
                    text = idioma,
                    data = {
                        'uf' : uf,
                        'idioma' : idioma
                    },                                        
                    on_click = self.selecionar_idioma
                ) for idioma, uf in LetrasServices._LINGUAGENS_DIPONIVEIS.items()
            ]
        )

        self.letra = ft.Container(
            alignment = ft.alignment.center,
            expand = True,
            
            content = ft.Text(
                size = 18,
                weight = ft.FontWeight.W_500,

                value = 'Nenhuma letra foi traduzida ainda'
            )
        )

        self.content = ft.Column(
            expand = True,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.Row(
                    height = 75,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 30,
                    controls = [
                        ft.Text(
                            value = 'Selecione um idioma',
                            size = 26,
                            weight = ft.FontWeight.BOLD
                        ),
                        self.infos
                    ]
                ),
                self.letra
            ]
        )

    def selecionar_idioma(self, e):
        LetrasServices.TRADUTOR.target = e.control.data.get('uf')
        
        self.letra.content.value = LetrasServices.executar_traducao(e.control.data.get('idioma'))
        self.letra. update()