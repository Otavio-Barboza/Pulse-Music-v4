# imports gerais
from enum import Enum
import inspect, asyncio


class GridMode(Enum):
    ARTIST = 'artist'
    ALBUM = 'album'
    
    
class GridState:

    # current_mode: GridMode | None = None
    # open_grid_playlist: bool = False
    _callbacks = {}

    
    @classmethod
    def register_callback(cls, event: str, func: callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(func)
        
    @classmethod
    def notify(cls, event: str, data = None):
        if event not in cls._callbacks:
            print(f'Evento de atualização não existente: {event}')
            return
        for func in cls._callbacks[event]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(data) if data is not None else func())
                else:
                    res = func(data) if data is not None else func()
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                print(e)

    # @classmethod
    # def set_current_mode(cls, mode: GridMode):
    #     cls.current_mode = mode

    # @classmethod
    # def set_open_grid_playlist(cls, value: bool):
    #     cls.open_grid_playlist = value