import threading

class AudioLoop:
    _iniciado = False
    player = None

    @classmethod
    def iniciar(cls):
        if cls._iniciado:
            return
        cls._iniciado = True

        threading.Thread(
            target=cls._run,
            daemon=True
        ).start()

    @classmethod
    def _run(cls):
        import pyglet

        cls.player = pyglet.media.Player()

        @cls.player.event
        def on_eos():
            from .monitor import Monitor
            Monitor.notificar_fim()

        pyglet.app.run()