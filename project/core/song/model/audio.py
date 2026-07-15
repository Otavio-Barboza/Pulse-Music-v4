# import de back-end
from project.core.song.model.monitoring import Monitoring

# import geral
import threading
import pyglet as pyg


class AudioLoop:

    _initialized: bool = False
    player: pyg.media.Player | None = None

    @classmethod
    def set_player(cls, content: pyg.media.Player):
        cls.player = content
        
    @classmethod
    def start(cls):
        if cls._initialized:
            return
        
        cls._initialized = True

        threading.Thread(
            target = cls._run,
            daemon = True
        ).start()

    @classmethod
    def _run(cls):
        cls.player = pyg.media.Player()

        @cls.player.event
        def on_eos():
            Monitoring.notify_end()

        pyg.app.run()