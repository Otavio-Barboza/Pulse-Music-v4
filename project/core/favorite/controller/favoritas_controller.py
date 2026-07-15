# imports de back-end
from core.song.model.song import Song
from core.song.model.reproduction import Reproduction
from core.song.enum.song_enum import ReproductionMode
from core.favorite.repository.favorite_repository import FavoriteRepository
from core.favorite.enum.favorite_enum import Favorited
from core.utils.utils import Utils

# import geral
import inspect, asyncio


class FavoriteState:

    _callbacks: dict[str, list] = {}

    # lista com objetos Song
    favorite_list: list[Song] = []

    @classmethod
    def register_callback(cls, event: str, callback : callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(callback)

    @classmethod
    def notify(cls, event: str, data = None):

        if event not in cls._callbacks:
            return
        
        for func in cls._callbacks[event]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(data))
                else:
                    res = func(data)
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                import traceback
                print(f"[CALLBACK ERROR]: {e}")
                traceback.print_exc()

    @classmethod
    def list_favorited_objects(cls) -> list[Song]:
        return FavoriteRepository.list_favorite_objects()
    
    @classmethod
    def convert_object_to_json(cls, data: Song):
        nova_chave, novo_item = FavoriteRepository.format_object_in_json(
            dado = data, 
            status = Favorited.FAVORITED.value
        )

        json_musicas = FavoriteRepository.ler_json()

        if nova_chave not in json_musicas:
            json_musicas[nova_chave] = novo_item

        Utils.sync_update_json(json_musicas)

        data.mode = ReproductionMode.FAVORITA.value

        cls.notify(
            evento = 'add_to_favorites',
            data = data
        )

    @classmethod
    def remove_favorite_json(cls, data: Song):
        json_favorita = FavoriteRepository.ler_json()
        chave_para_remover = None

        for chave, _ in json_favorita.items():
            if chave == data.chave:
                chave_para_remover = chave
                break
        
        if chave_para_remover is None:
            return 
        
        del json_favorita[chave_para_remover]
        FavoriteRepository.salvar_json(json_favorita)

        cls.notify(
            'unfavorite',
            data
        )  
        
    @classmethod
    def list_favorite(cls) -> list[str]:
        return FavoriteRepository.list_favorite()
    
    @classmethod
    def add_music_to_playback(cls, song : Song):
        Reproduction.add_song(song)

    @classmethod
    def remove_music_to_playback(cls, song : Song):
        Reproduction.remove_song(song)