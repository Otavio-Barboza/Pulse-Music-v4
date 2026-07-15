# imports do back-end
from core.playlists.repository.playlist_repository import PlaylistRepository
from core.playlists.enum.playlist_enum import PlaylistLoaded

# imports gerais
import inspect, asyncio


class PlaylistState:
    playlist_loaded = PlaylistLoaded.CLOSE
    _callbacks = {}

    @classmethod
    def registet_callback(cls, event: str, function: callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(function)
        
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
    def open_playlist(cls, id: str, status: PlaylistLoaded):
        cls.playlist_loaded = {
            'id' : id,
            'open_or_close' : status
        }

    @classmethod
    def close_playlist(cls):
        cls.playlist_loaded = PlaylistLoaded.CLOSE

    @classmethod
    def return_music_artist(cls, id: str) -> str:
        return PlaylistRepository.identify_music_artist(id)
    
    @classmethod
    def return_cover(cls, music_name: str) -> str:
        return PlaylistRepository.return_cover(music_name)