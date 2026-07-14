# imports gerais
import inspect, asyncio


class ScannerController:
    _callbacks = {}
    
    @classmethod
    def register_callback(cls, event: str, function : callable):
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