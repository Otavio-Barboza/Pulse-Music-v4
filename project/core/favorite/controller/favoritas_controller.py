# imports de back-end
from core.song.model.song import Song
from core.song.model.reproduction import Reproduction
from core.song.enum.song_enum import ReproductionMode
from core.favorite.repository.favorite_repository import FavoriteRepository
from core.favorite.enum.favorite_enum import Favorited
from core.utils.utils import Utils
from core.utils.path import AppPaths
from core.services.account_manager import AccountManager

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
        new_key, new_item = FavoriteRepository.format_object_in_json(
            data = data, 
            status = Favorited.FAVORITED.value
        )

        favorites_json: dict = Utils.sync_load_json(
            AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "favorites.json"
        )

        if new_key not in favorites_json:
            favorites_json[new_key] = new_item

        Utils.sync_update_json(
            path = AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "favorites.json", 
            data = favorites_json
        )

        data.mode = ReproductionMode.FAVORITE.value

        cls.notify(
            event = 'add_to_favorites',
            data = data
        )

    @classmethod
    def remove_favorite_json(cls, data: Song):
        favorites_json: dict = Utils.sync_load_json(
            AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "favorites.json"
        )
        key_to_remove = None

        for key, _ in favorites_json.items():
            if key == data.key:
                key_to_remove = key
                break
        
        if key_to_remove is None:
            return 
        
        del favorites_json[key_to_remove]
        Utils.sync_update_json(
            path = AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "favorites.json",
            data = favorites_json
        )

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