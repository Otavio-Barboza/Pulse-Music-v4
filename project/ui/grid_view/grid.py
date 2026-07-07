from project.ui.others.overlay_images import OverlayImages
from ...App.Services.Controllers.estado_grid import GridMode, EstadoGrid
from ...App.Meta.Memoria.memoria_global import memoria
from ...App.Meta.Repository.extrai_metadados import ExtracaoMetadados
from ...App.Audio.Model.modo_reproducao import ModoReprodução
import flet as ft
import os

class GridImages(ft.GridView):
    def __init__(self, modo : GridMode, caminho : str):
        super().__init__(
            max_extent = 200 if modo == GridMode.ARTISTA else 250,
            expand = True,
            spacing = 65,
            run_spacing = 15,
            padding = ft.padding.all(15)
        )
        self.modo = modo

        self.controls = []
        self.reconstruir_imagens(self.modo)
        
        EstadoGrid.registrar_callback(
            evento = 'att_grid',
            func = self.reconstruir_imagens
        )
    
    def click(self, e):
        from ...App.Audio.Model.musica import Musica
        from ...App.Audio.Model.modo_reproducao import Reprodução
        
        lista_mus = []
        
        if self.modo == GridMode.ARTISTA:
            modo_playlist = ModoReprodução.ARTISTA
            dados = memoria.artistas.to_dict()
            
            for chave, musica in dados.get(e.control.data).items():
                if chave == 'musicas':
                    for mus in musica:
                        lista_mus.append(
                            Musica(
                                modo = modo_playlist,
                                nome = os.path.basename(
                                    mus.get('caminho_completo')
                                ).replace(
                                    '.mp3', ''
                                ),
                                caminho = mus.get('caminho_completo'),
                                chave = mus.get('chave')
                            )
                        )
                
            caminho = dados.get(e.control.data).get('musicas')[0].get('caminho_completo')
            img = ExtracaoMetadados.carregar_imagem_big_base64(
                caminho_arquivo = caminho, 
                tipo = 'artist'
            )
            nome = dados.get(e.control.data).get('nome_artistas')
        else:
            modo_playlist = ModoReprodução.ALBUM
            dados = memoria.albuns.to_dict()
            
            for musica in dados.get(e.control.data).values():
                for caminho_musica in musica:
                    lista_mus.append(
                        Musica(
                            modo = ModoReprodução.ALBUM,
                            
                            nome = os.path.basename(
                                caminho_musica.get('caminho_da_musica_completa')
                            ).replace('.mp3', ''),
                            
                            caminho = os.path.normpath(
                                caminho_musica.get('caminho_da_musica_completa')
                            ),
                            
                            chave = caminho_musica.get('chave_da_musica')
                        ) 
                    )                

            for musica in lista_mus:
                if musica.caminho is not None:
                    caminho = musica.caminho
                    break
                
            img = ExtracaoMetadados.carregar_imagem_big_base64(
                caminho_arquivo = caminho, 
                tipo = 'album'
            )
            nome = e.control.data

        self.page.overlay.clear()
        self.page.overlay.append(
            OverlayImages(
                img_big = img,
                musicas = lista_mus,
                modo = self.modo,
                nome = nome,
                modo_playlist = modo_playlist
            )
        )
        self.page.update()
        
        Reprodução.carregar_musicas_do_modo(
            modo = modo_playlist,
            lista = lista_mus
        )


    def reconstruir_imagens(self, modo : GridMode):
        from ...App.Services.gerenciador_contas import GerenciadorContas
        import os
        
        if modo != self.modo:
            return
        
        caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/{"Artistas" if modo == GridMode.ARTISTA else "Albuns"}'
        
        self.controls.clear()
        
        for img in os.listdir(caminho):
            chave_img = img.removesuffix('.jpg')
            
            if self.modo == GridMode.ARTISTA:
                nome = memoria.artistas.to_dict().get(chave_img).get('nome_artistas')
            else:
                nome = chave_img
                
            self.controls.extend([
                ft.Container(
                    data = chave_img,
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
                                weight = ft.FontWeight.W_300,
                                max_lines = 2,
                                overflow = ft.TextOverflow.FADE
                            )
                        ]
                    )
                )
            ])

class Imagem(ft.Image):
    def __init__(self, src : str, modo : GridMode):
        super().__init__(
            src = src if src else r'',
            border_radius = ft.border_radius.all(100) if modo == GridMode.ARTISTA else ft.border_radius.all(7.5),
            filter_quality = ft.FilterQuality.HIGH,
            fit = ft.ImageFit.COVER
        )