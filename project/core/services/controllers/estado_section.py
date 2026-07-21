class StateSection:
    
    state = {
        'view' : []
    }
    _callbacks = {
        'view' : []
    }

    @classmethod
    def register(cls, key : str, callback : callable):
        if key not in cls._callbacks:
            cls._callbacks[key] = []
        
        if callback not in cls._callbacks[key]:
            cls._callbacks[key].append(callback)

    @classmethod
    def remove(cls, key : str, callback : callable):
        if key in cls._callbacks:
            if callback in cls._callbacks[key]:
                cls._callbacks[key].remove(callback)

    @classmethod
    def alter_view(cls, key : str, value):
        cls.state[key] = value
        cls.notify(key = key, value = value)

    @classmethod
    def notify(cls, key : str, value):
        for callback in list(cls._callbacks.get(key, [])):
            try:
                callback(value)
            except Exception:
                pass