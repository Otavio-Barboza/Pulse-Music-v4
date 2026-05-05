from .cores import cor
from ...App.Services.Controllers.estado_grid import GridMode
import flet as ft
import os

class OverlayImagens(ft.Container):
    def __init__(self, modo : GridMode, img_big : str, nomes : list, nome : str):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            padding = ft.padding.all(15),
            bgcolor = cor.preto2
        )
        self.modo = modo
        self.nome = nome

        self.content = ft.ResponsiveRow(
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.SPACE_EVENLY,
            run_spacing = 10,
            spacing = 10, 
            # expand = True,

            controls = [
                ft.Container(
                    col = {'md' : 5, 'sm' : 12},
                    expand = True,

                    content = ft.Column(
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.CENTER,

                        controls = [
                            ft.Image(
                                src_base64 = img_big,
                                border_radius = ft.border_radius.all(10) if self.modo == GridMode.ARTISTA else ft.border_radius.all(10),
                                fit = ft.ImageFit.COVER
                            ),
                            ft.Text(
                                value = nome,
                                text_align = ft.TextAlign.CENTER,
                                size = 26,
                                weight = ft.FontWeight.W_500
                            )
                        ]
                    )
                ),

                ft.Container(
                    col = {'md' : 7, 'sm' : 12},
                    bgcolor = cor.preto9,
                    padding = ft.padding.only(
                        top = 15,
                        bottom = 15,
                        left = 10,
                        right = 10
                    ),
                    border_radius = ft.border_radius.all(20) if self.modo == GridMode.ARTISTA else ft.border_radius.all(10),
                    alignment = ft.alignment.top_center,

                    content = ft.Column(
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.START,

                        controls = [
                            ft.Text(
                                value = f'Músicas do{"(a)" if self.modo == GridMode.ARTISTA else ""} {"artista" if self.modo == GridMode.ARTISTA else "álbum"}',
                                size = 18,
                                weight = ft.FontWeight.W_500,
                                text_align = ft.TextAlign.CENTER
                            ),

                            ft.Column( 
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                alignment = ft.MainAxisAlignment.CENTER,
                                scroll = ft.ScrollMode.AUTO,

                                controls = [
                                    ft.Container(
                                        alignment = ft.alignment.center,
                                        bgcolor = cor.preto_puro_5,
                                        border_radius = ft.border_radius.all(15) if self.modo == GridMode.ARTISTA else ft.border_radius.all(5),
                                        padding = ft.padding.all(10),

                                        content = ft.Text(
                                            value = os.path.basename(i.removesuffix('.mp3')),
                                            text_align = ft.TextAlign.LEFT,
                                            size = 18,
                                            max_lines = 2
                                        ) 
                                    ) for i in nomes
                                ]
                            )
                        ]
                    )
                )
            ]
        )