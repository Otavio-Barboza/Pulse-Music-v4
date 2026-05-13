from ...App.Services.Controllers.estado_grid import GridMode, EstadoGrid
from ..Others.overlay_imagens import OverlayImagens
from ...App.Meta.Memoria.memoria_global import memoria
from ...App.Meta.Repository.extrai_metadados import ExtracaoMetadados
import flet as ft
import os

class GridImagens(ft.GridView):
    def __init__(self, page, modo : GridMode, caminho : str):
        super().__init__(
            max_extent = 200 if modo == GridMode.ARTISTA else 250,
            expand = True,
            spacing = 45,
            run_spacing = 20 if modo == GridMode.ARTISTA else 10,
            padding = ft.padding.all(15)
        )
        self.page = page
        self.modo = modo

        self.controls = [
            ft.Container(
                data = img.removesuffix('.jpg'),
                on_click = self.click,

                content = ft.Column(
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.START,

                    controls = [
                        Imagem(
                            src = f'{caminho}/{img}', 
                            modo = modo
                        ),
                        ft.Text(
                            value = img.removesuffix('.jpg'),
                            text_align = ft.TextAlign.CENTER,
                            size = 16,
                            weight = ft.FontWeight.W_300
                        )
                    ]
                )
            ) for img in os.listdir(caminho)
        ]
        
        EstadoGrid.registrar_callback(
            evento = 'att_grid',
            func = self.reconstruir_imagens
        )
    
    def click(self, e):        
        if self.modo == GridMode.ARTISTA:
            dados = memoria.artistas.to_dict()
            caminho = dados.get()
            img = ExtracaoMetadados.carregar_imagem_big_base64(
                caminho_arquivo = lista_mus[-1], 
                tipo = 'artist'
            )
        else:
            lista_mus = memoria.albuns.albuns.get(e.control.data).get('musicas')
            img = ExtracaoMetadados.carregar_imagem_big_base64(
                caminho_arquivo = lista_mus[-1], 
                tipo = 'album'
            )

        self.page.overlay.clear()
        self.page.overlay.append(
            OverlayImagens(
                img_big = img,
                nomes = lista_mus,
                modo = self.modo,
                nome = e.control.data
            )
        )
        self.page.update()

    def reconstruir_imagens(self, modo : GridMode):
        from ...App.Services.gerenciador_contas import GerenciadorContas
        import os
        
        if modo != self.modo:
            return
        
        caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/{"Artistas" if modo == GridMode.ARTISTA else "Albuns"}'
        
        self.controls.clear()
        
        for img in os.listdir(caminho):
            if self.modo == GridMode.ARTISTA:
                nome = memoria.artistas.to_dict().get(
                    img.removesuffix('.jpg')
                ).get('nome_artistas')
            else:
                nome = img.removesuffix('.jpg')
                
            self.controls.extend([
                ft.Container(
                    data = img.removesuffix('.jpg'),
                    on_click = self.click,

                    content = ft.Column(
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.START,

                        controls = [
                            Imagem(
                                src = f'{caminho}/{img}', 
                                modo = self.modo
                            ),
                            ft.Text(
                                value = nome,
                                text_align = ft.TextAlign.CENTER,
                                size = 16,
                                weight = ft.FontWeight.W_300
                            )
                        ]
                    )
                )
            ])
        
        self.update()
        
class Imagem(ft.Image):
    def __init__(self, src : str, modo : GridMode):
        super().__init__(
            src = src if src else r'',
            border_radius = ft.border_radius.all(100) if modo == GridMode.ARTISTA else ft.border_radius.all(7.5),
            filter_quality = ft.FilterQuality.HIGH,
            fit = ft.ImageFit.COVER
        )