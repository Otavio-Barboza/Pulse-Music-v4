# import de interface
from project.ui.others.colors import color

# import de back-end
from ... import LetrasServices

# import geral
import flet as ft


class TranslationContent(ft.Container):
    def __init__(self):
        super().__init__(
            padding = ft.padding.only(right = 30, left = 10),
            margin = ft.margin.only(bottom = 10),
            expand = True,
            alignment = ft.alignment.center
        )

        self.infos = ft.PopupMenuButton(
            icon = ft.Icons.G_TRANSLATE,
            icon_color = color.preto3,
            surface_tint_color = color.branco,
            bgcolor = color.preto3,
            shadow_color = color.branco,
            tooltip = "Idiomas",

            style = ft.ButtonStyle(
                color = {
                    ft.ControlState.DEFAULT : color.azul_medio2,
                    ft.ControlState.HOVERED : color.azul_medio
                },
                overlay_color = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.DEFAULT : color.branco
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

                value = self.carregar_letra()
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

    def carregar_letra(self):
        from .....App.Letras.Cache.memoria_letras import LetrasMemoria

        if LetrasMemoria._cache_letra is None:
            return 'Nenhuma letra carregada para tradução'
        else:
            return LetrasServices.executar_traducao(LetrasMemoria._cache_letra)

    def selecionar_idioma(self, e):
        from .....App.Letras.Cache.memoria_letras import LetrasMemoria

        LetrasMemoria.atualizar_cache(e.control.data.get('idioma'))
        LetrasServices.TRADUTOR.target = e.control.data.get('uf')
        
        self.letra.content.value = LetrasServices.executar_traducao(e.control.data.get('idioma'))
        self.update()