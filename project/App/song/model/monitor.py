import threading

class Monitor:
    @classmethod
    def notificar_fim(cls):
        from ..Controller.sessao import SessaoReproducao
        SessaoReproducao.tratar_fim_da_musica()