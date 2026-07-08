# imports de back-end
from project.core.song.model.song import Song
from project.core.song.enum.song_enum import ReproductionMode
from ...Meta.Repository.tarefas import ManagesMetadata
from project.core.utils.utils import Utils
from project.core.services.account_manager import AccountManager

# imports gerais
from pathlib import Path
import os


class SongRepository:

    @classmethod
    def load_songs(cls, path: Path, mode: ReproductionMode) -> list[Song]:
        return [
            Song(
                name = song.removesuffix('.mp3'),
                path = os.path.normpath(
                    os.path.join(path, song)
                ),
                key = ManagesMetadata.gerar_track_id(
                    os.path.normpath(
                        os.path.join(path, song)
                    )
                ),
                mode = mode
            ) for song in os.listdir(path)
        ]

    @classmethod
    def get_artist(cls, key_song : str):
        song_json: dict = Utils.sync_load_json(f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Song/musicas.json')
        
        key: str
        item: dict
    
        for key, item in song_json.items():
            if key == key_song:
                artista = item.get('artista_final')
                return artista if artista is not None else 'Artista Desconhecido'
            
    @classmethod
    def get_cover(cls, song : str):    
        cover: str

        for cover in os.listdir(
            f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Imagens/Capa Song'
        ):
            if cover.removesuffix('.jpg') == song:
                return os.path.normpath(
                    os.path.join(
                        f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Imagens/Capa Song',
                        cover
                    )
                )
        else:
            return r'Assets\Global\Images\Padrao\capa_musicas_desconhecidas.png'
    
    @classmethod
    def get_song(cls, key_song : str):
        song_json = Utils.sync_load_json(f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Song/musicas.json')
        
        key: str
        item: dict

        for key, item in song_json.items():
            if key == key_song:
                song = item
                break

        if song['nome_musica_filtrado'].get('titulo_ID3_filtrado') is not None:
            return song['nome_musica_filtrado'].get('titulo_ID3_filtrado')
        elif song['nome_musica_filtrado'].get('arquivo_mp3_filtrado') is not None:
            return song['nome_musica_filtrado'].get('arquivo_mp3_filtrado')
        elif song['titulo_ID3_original'] is not None:
            return song.get('titulo_ID3_original')
        else:
            return song.get('arquivo_original')