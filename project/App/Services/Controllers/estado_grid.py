from enum import Enum
from typing import Callable
import inspect, asyncio

class GridMode(Enum):
    ARTISTA = 'artista'
    ALBUM = 'album'
    
class EstadoGrid:
    _callbacks = {}
    
    @classmethod
    def registrar_callback(cls, evento : str, func : callable):
        if evento not in cls._callbacks:
            cls._callbacks[evento] = []
        cls._callbacks[evento].append(func)
        
    @classmethod
    def _notificar(cls, evento : str, dados = None):
        if evento not in cls._callbacks:
            raise(f'Evento de atualização não existente: {evento}')
        
        for func in cls._callbacks[evento]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(dados) if dados is not None else func())
                else:
                    res = func(dados) if dados is not None else func()
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                print(e)