from .cores import cor
from ...App.Services.Controllers.estado_grid import GridMode
from ..Playlist.Base.list_musicas import ListViewMusicas
import flet as ft
import os

class OverlayImagens(ft.Container):
    def __init__(
        self, 
        modo_playlist,
        modo : GridMode, 
        img_big : str, 
        musicas : list, 
        nome : str,
    ):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            padding = ft.padding.all(15),
            bgcolor = cor.preto2
        )
        
        self.modo_playlist = modo_playlist
        self.modo = modo
        self.musicas = musicas

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
                    bgcolor = cor.preto8,
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

                            ft.Container(
                                content = ListViewMusicas(
                                    page = self.page,
                                    musicas = self.musicas,
                                    modo_favorita = None
                                )
                            )
                        ]
                    )
                )
            ]
        )