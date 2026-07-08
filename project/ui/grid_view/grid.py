# import de interface
from project.ui.others.overlay_images import OverlayImages

# imports de back-end
from project.core.services.controllers.grid_state import GridMode, GridState
from project.core.song.enum.song_enum import ReproductionMode
from ...App.Meta.Memoria.memoria_global import memoria
from ...App.Meta.Repository.extrai_metadados import ExtracaoMetadados
from project.core.services.account_manager import AccountManager

# imports gerais
import flet as ft
import os

class GridImages(ft.GridView):
    def __init__(self, modo : GridMode, caminho : str):
        super().__init__(
            max_extent = 200 if modo == GridMode.ARTIST else 250,
            expand = True,
            spacing = 65,
            run_spacing = 15,
            padding = ft.padding.all(15)
        )

        self.modo = modo

        self.controls = []
        self.reconstruir_imagens(self.modo)
        
        GridState.register_callback(
            event = 'att_grid',
            function = self.reconstruir_imagens
        )
    
    def click(self, e):
        from project.core.song.model.song import Song
        from project.core.song.model.reproduction import Reproduction
        
        lista_mus = []
        
        if self.modo == GridMode.ARTIST:
            modo_playlist = ReproductionMode.ARTIST
            dados = memoria.artistas.to_dict()
            
            for chave, musica in dados.get(e.control.data).items():
                if chave == 'musicas':
                    for mus in musica:
                        lista_mus.append(
                            Song(
                                mode = modo_playlist,
                                name = os.path.basename(
                                    mus.get('caminho_completo')
                                ).replace(
                                    '.mp3', ''
                                ),
                                path = mus.get('caminho_completo'),
                                key = mus.get('key')
                            )
                        )
                
            caminho = dados.get(e.control.data).get('musicas')[0].get('caminho_completo')
            img = ExtracaoMetadados.carregar_imagem_big_base64(
                caminho_arquivo = caminho, 
                tipo = 'artist'
            )
            nome = dados.get(e.control.data).get('nome_artistas')
        else:
            modo_playlist = ReproductionMode.ALBUM
            dados = memoria.albuns.to_dict()
            
            for musica in dados.get(e.control.data).values():
                for caminho_musica in musica:
                    lista_mus.append(
                        Song(
                            mode = ReproductionMode.ALBUM,
                            
                            name = os.path.basename(
                                caminho_musica.get('caminho_da_musica_completa')
                            ).replace('.mp3', ''),
                            
                            path = os.path.normpath(
                                caminho_musica.get('caminho_da_musica_completa')
                            ),
                            
                            key = caminho_musica.get('chave_da_musica')
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
                image_big = img,
                music = lista_mus,
                mode = self.modo,
                name = nome,
                playlist_mode = modo_playlist
            )
        )
        self.page.update()
        
        Reproduction.load_songs_from_mode(
            modo = modo_playlist,
            lista = lista_mus
        )


    def reconstruir_imagens(self, modo : GridMode):
        
        if modo != self.modo:
            return
        
        caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/{"Artistas" if modo == GridMode.ARTIST else "Albuns"}'
        
        self.controls.clear()
        
        for img in os.listdir(caminho):
            chave_img = img.removesuffix('.jpg')
            
            if self.modo == GridMode.ARTIST:
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
            border_radius = ft.border_radius.all(100) if modo == GridMode.ARTIST else ft.border_radius.all(7.5),
            filter_quality = ft.FilterQuality.HIGH,
            fit = ft.ImageFit.COVER
        )