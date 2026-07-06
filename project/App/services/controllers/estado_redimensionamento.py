class ResizeManager:
    _callbacks = []

    @classmethod
    def registrar(cls, func):
        cls._callbacks.append(func)

    @classmethod
    def executar(cls, e):
        for f in cls._callbacks:
            try:
                f(e)
            except Exception:
                pass
    
    @classmethod
    def remover(cls, call):
        if call in cls._callbacks:
            cls._callbacks.remove(call)