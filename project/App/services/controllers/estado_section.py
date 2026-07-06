class EstadoSection:
    view_atual = None
    _estado = {
        'view' : []
    }
    _observadores = {
        'view' : []
    }

    @classmethod
    def registrar(cls, chave : str, callback : callable):
        if chave not in cls._observadores:
            cls._observadores[chave] = []
        
        if callback not in cls._observadores[chave]:
            cls._observadores[chave].append(callback)

    @classmethod
    def remover(cls, chave : str, callback : callable):
        if chave in cls._observadores:
            if callback in cls._observadores[chave]:
                cls._observadores[chave].remove(callback)

    @classmethod
    def alterar(cls, chave : str, valor):
        cls._estado[chave] = valor
        cls._notificar(chave = chave, valor = valor)

    @classmethod
    def _notificar(cls, chave : str, valor):
        for callback in list(cls._observadores.get(chave, [])):
            try:
                callback(valor)
            except Exception:
                pass