class ResizeManager:
    _callbacks = []

    @classmethod
    def register(cls, func):
        cls._callbacks.append(func)

    @classmethod
    def to_execute(cls, event):
        for function in cls._callbacks:
            try:
                function(event)
            except Exception:
                pass
    
    @classmethod
    def remove(cls, call):
        if call in cls._callbacks:
            cls._callbacks.remove(call)