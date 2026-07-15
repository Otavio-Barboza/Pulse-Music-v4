# import de interface
from ui.others.overlay_images import OverlayImages

# imports de back-end
from core.services.controllers.grid_state import GridMode, GridState
from core.song.enum.song_enum import ReproductionMode
from core.meta.cache.global_cache import cache_metadata
from core.meta.repository.extract_metadata import ExtractMetadata
from core.services.account_manager import AccountManager
from core.utils.path import AppPaths

# imports gerais
from pathlib import Path
import flet as ft
import os


class GridImages(ft.GridView):
    def __init__(self, mode: GridMode, path : str):
        super().__init__(
            max_extent = 200 if mode == GridMode.ARTIST else 250,
            expand = True,
            spacing = 65,
            run_spacing = 15,
            padding = ft.padding.all(15)
        )

        self.mode = mode

        self.controls = []
        self.build_images(self.mode)
        
        GridState.register_callback(
            event = 'att_grid',
            func = self.build_images
        )
    
    def click(self, e):
        from core.song.model.song import Song
        from core.song.model.reproduction import Reproduction
        
        song_list = []
        
        if self.mode == GridMode.ARTIST:
            modo_playlist = ReproductionMode.ARTIST
            dados = cache_metadata.artists.to_dict()
            
            for key, song in dados.get(e.control.data).items():
                if key == 'songs':
                    for music in song:
                        song_list.append(
                            Song(
                                mode = modo_playlist,
                                name = os.path.basename(
                                    music.get('caminho_completo')
                                ).replace(
                                    '.mp3', ''
                                ),
                                path = music.get('caminho_completo'),
                                key = music.get('key')
                            )
                        )
                
            path = dados.get(e.control.data).get('songs')[0].get('caminho_completo')
            img = ExtractMetadata.load_image_big_base64(
                caminho_arquivo = path, 
                tipo = 'artist'
            )
            nome = dados.get(e.control.data).get('nome_artistas')
        else:
            modo_playlist = ReproductionMode.ALBUM
            dados = cache_metadata.albums.to_dict()
            
            for song in dados.get(e.control.data).values():
                for song_path in song:
                    song_list.append(
                        Song(
                            mode = ReproductionMode.ALBUM,
                            
                            name = os.path.basename(
                                song_path.get('caminho_da_musica_completa')
                            ).replace('.mp3', ''),
                            
                            path = os.path.normpath(
                                song_path.get('caminho_da_musica_completa')
                            ),
                            
                            key = song_path.get('chave_da_musica')
                        ) 
                    )                

            for song in song_list:
                if song.path is not None:
                    path = song.path
                    break
                
            img = ExtractMetadata.load_image_big_base64(
                caminho_arquivo = path, 
                tipo = 'album'
            )
            nome = e.control.data

        self.page.overlay.clear()
        self.page.overlay.append(
            OverlayImages(
                image_big = img,
                music = song_list,
                mode = self.mode,
                name = nome,
                playlist_mode = modo_playlist
            )
        )
        self.page.update()
        
        Reproduction.load_songs_from_mode(
            mode = modo_playlist,
            lista = song_list
        )

    def build_images(self, mode: GridMode):    
        if mode != self.mode:
            return
        
        # path = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/{"Artistas" if mode == GridMode.ARTIST else "Albuns"}'
        if mode == GridMode.ARTIST:
            path: Path = AppPaths.ACCOUNT / str(AccountManager.accounts_cache.get("current_account")) / "images" / "artists"
        elif mode == GridMode.ALBUM:
            path: Path = AppPaths.ACCOUNT / str(AccountManager.accounts_cache.get("current_account")) / "images" / "albums"
        else:
            ...
            
        print(path)
        self.controls.clear()
        
        for img in os.listdir(path):
            image_key = img.removesuffix('.jpg')
            
            if self.mode == GridMode.ARTIST:
                nome = cache_metadata.artists.to_dict().get(image_key).get('nome_artistas')
            else:
                nome = image_key
                
            self.controls.extend([
                ft.Container(
                    data = image_key,
                    on_click = self.click,

                    content = ft.Column(
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.START,

                        controls = [
                            Imagem(
                                src = f'{path}/{img}', 
                                mode = self.mode
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
    def __init__(self, src : str, mode : GridMode):
        super().__init__(
            src = src if src else r'',
            border_radius = ft.border_radius.all(100) if mode == GridMode.ARTIST else ft.border_radius.all(7.5),
            filter_quality = ft.FilterQuality.HIGH,
            fit = ft.ImageFit.COVER
        )