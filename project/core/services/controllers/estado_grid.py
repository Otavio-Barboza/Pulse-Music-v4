from enum import Enum
import inspect, asyncio

class GridMode(Enum):
    ARTIST = 'artist'
    ALBUM = 'album'
    
class GridState:
    _callbacks = {}
    
    @classmethod
    def registrar_callback(cls, event: str, func: callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(func)
        
    @classmethod
    def notify(cls, event : str, dados = None):
        if event not in cls._callbacks:
            raise(f'Evento de atualização não existente: {event}')
        
        for func in cls._callbacks[event]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(dados) if dados is not None else func())
                else:
                    res = func(dados) if dados is not None else func()
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                print(e)