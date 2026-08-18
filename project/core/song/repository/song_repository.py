# imports de back-end
from core.song.model.song import Song
from core.song.enum.song_enum import ReproductionMode
from core.meta.repository.tasks import Task
from core.meta.cache.global_cache import cache_metadata
from core.services.account_manager import AccountManager
from core.utils.utils import Utils

# imports gerais
from pathlib import Path
import os


class SongRepository:

    @classmethod
    def load_songs(cls, path: Path, mode: ReproductionMode) -> list[Song]:
        if isinstance(path, str):
            path = Path(path)
        
        music_list_path: list[str] = [
            str(path / song)
            for song in os.listdir(path)
        ]
        music_list_json: list[str] = [
            key
            for key, value in cache_metadata.tracks.items()
            if value.get("song_path") == str(path)
        ]

        if len(music_list_path) > len(music_list_json):
            return [
                Song(
                    name = song.removesuffix('.mp3'),
                    path = path / song,
                    key = Task.return_track_id(path / song),
                    mode = mode
                ) for song in sorted(os.listdir(path), key = str.casefold)
            ]
        else:
            return [
                Song(
                    name = value.get("mp3_file").removesuffix(".mp3"),
                    path = str(value.get("song_path")),
                    key = key,
                    mode = mode
                ) for key, value in sorted(
                    cache_metadata.tracks.items(), 
                    key = lambda item: item[1].get("mp3_file").casefold()
                ) if value.get("song_path") == str(path)
            ]


    # Onde é chamadas essas funções?
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
    def get_cover(cls, song: str):    
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
    def get_song(cls, key_song: str):
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