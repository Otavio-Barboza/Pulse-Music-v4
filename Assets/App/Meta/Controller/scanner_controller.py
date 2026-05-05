import inspect, asyncio

class ScannerController:
    _callbacks = {}
    
    @classmethod
    def registar_callback(cls, evento : str, funcao : callable):
        if evento not in cls._callbacks:
            cls._callbacks[evento] = []
        cls._callbacks[evento].append(funcao)
        
    @classmethod
    def notificar(cls, evento : str, dados = None):
        if evento not in cls._callbacks:
            return
        
        for func in cls._callbacks[evento]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(dados))
                else:
                    res = func(dados)
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                import traceback

                print(f"[CALLBACK ERROR]: {e}")
                traceback.print_exc()