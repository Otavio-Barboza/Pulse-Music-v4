from core.song.model.monitoring import Monitoring
from core.song.model.audio import AudioLoop

# imports gerais
from pathlib import Path
import threading, pyglet


class Player:

    _volume = 1.0

    @classmethod
    def load_song(cls, path: Path):

        if not AudioLoop.player:
            return

        AudioLoop.player.pause()
        AudioLoop.player.delete()

        AudioLoop.set_player(pyglet.media.Player())

        @AudioLoop.player.event
        def on_eos():
            Monitoring.notify_end()

        font: pyglet.media.Source | pyglet.media.StreamingSource = pyglet.media.load(str(path))
        AudioLoop.player.queue(font)

    @classmethod
    def play(cls):
        AudioLoop.player.play()

    @classmethod
    def pause(cls):
        AudioLoop.player.pause()

    @classmethod
    def stop(cls):
        AudioLoop.player.pause()
        AudioLoop.player.seek(0)
    
    @classmethod
    def formatted_total_duration(cls) -> str:
        font: float = cls.current_duration()
        
        minutes = int(font / 60)
        seconds = int(font - (minutes * 60))

        return f'{minutes:02}:{seconds:02}'

    @classmethod
    def formatted_current_duration(cls) -> str:
        font: float = cls.current_position()
        
        minutes = int(font / 60)
        seconds = int(font - (minutes * 60))
        
        return f'{minutes:02}:{seconds:02}' or f'00:00'
    
    @classmethod
    def current_position(cls) -> float:
        return AudioLoop.player.time
    
    @classmethod
    def current_duration(cls) -> float:
        return AudioLoop.player.source.duration

    @classmethod
    def set_volume(cls, volume: float):
        cls._volume = max(0.0, min(1.0, volume))
        AudioLoop.player.volume = cls._volume

    @classmethod
    def get_volume(cls):
        return cls._volume

    @classmethod
    def go_to(cls, seconds: float):
        AudioLoop.player.seek(seconds)