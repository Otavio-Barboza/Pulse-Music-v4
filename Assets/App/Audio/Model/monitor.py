class Monitor:
    @classmethod
    def notificar_fim(cls):
        from ..Controller.estado_musica import EstadoMusica
        EstadoMusica.tratar_fim_musica()

import threading

class MonitorTempo(threading.Thread):
    def __init__(self, estado, intervalo=0.2):
        super().__init__(daemon=True)
        self.estado = estado
        self.intervalo = intervalo
        self._ativo = True

    def run(self):
        from ..Model.reprodutor import Reprodutor
        import time
        
        while self._ativo:
            if not self.estado.usuario_arrastando:
                tempo = Reprodutor.posicao_pura()
                self.estado.atualizar_tempo(tempo)
                
            time.sleep(self.intervalo)

    def parar(self):
        self._ativo = False
