from .monitor import Monitor
from .audio import AudioLoop
import threading, pyglet

class Reprodutor:
    _volume = 1.0

    @classmethod
    def carregar(cls, caminho: str):
        import pyglet

        player = AudioLoop.player
        if not player:
            return

        player.pause()
        player.delete()

        AudioLoop.player = pyglet.media.Player()

        @AudioLoop.player.event
        def on_eos():
            from .monitor import Monitor
            Monitor.notificar_fim()

        fonte = pyglet.media.load(caminho)
        AudioLoop.player.queue(fonte)

    @classmethod
    def tocar(cls):
        AudioLoop.player.play()

    @classmethod
    def pausar(cls):
        AudioLoop.player.pause()

    @classmethod
    def parar(cls):
        AudioLoop.player.pause()
        AudioLoop.player.seek(0)
    
    @classmethod
    def duracao(cls):
        fonte = AudioLoop.player.source
        minutos = int(fonte.duration / 60)
        segundos = int(fonte.duration - (minutos * 60))
        return f'{minutos:02}:{segundos:02}'

    @classmethod
    def posicao(cls):
        fonte = AudioLoop.player
        minutos = int(fonte.time / 60)
        segundos = int(fonte.time - (minutos * 60))
        return f'{minutos:02}:{segundos:02}' or f'00:00'
    
    @classmethod
    def posicao_pura(cls):
        return AudioLoop.player.time
    
    @classmethod
    def duracao_pura(cls):
        return AudioLoop.player.source.duration

    @classmethod
    def set_volume(cls, volume : float):
        cls._volume = max(0.0, min(1.0, volume))
        AudioLoop.player.volume = cls._volume

    @classmethod
    def get_volume(cls):
        return cls._volume

    @classmethod
    def ir_para(cls, segundos: float):
        AudioLoop.player.seek(segundos)