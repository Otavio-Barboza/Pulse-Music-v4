# import de back-end
from core.song.model.monitoring import Monitoring

# imports gerais
from multiprocessing import Process, Queue
import pyglet as pyg


_AUDIO_STATE: dict[str, float | bool] = {
    "position" : 0.0,
    "duration" : 0.0, 
    "is_playing" : False,
    "volume" : 1.0
}


def _run_audio_process(
    command_queue: Queue, 
    event_queue: Queue,
    state_queue: Queue
):
    """
    _summary_: (
        Executa o motor de áudio dentro de um processo separado.

        Este processo possui seu próprio pyglet.
        Player e seu próprio Event Loop. 
        Nenhum objeto do pyglet é compartilhado com o processo principal.
    )

    Args:
        command_queue (Queue): ...
        event_queue (Queue): ...
        state_queue (Queue): ...
    """

    # Player pertence exclusivamente ao processo de áudio.
    player = pyg.media.Player()
    volume = 1.0

    def notify_end_of_song():
        """
        _summary_: (
            Envia um evento para o processo principal informando
            que a música chegou ao fim.

            O processo de áudio não chama diretamente o
            ReproductionManager, Monitoring ou qualquer outra
            classe da aplicação principal.
        )
        """
        event_queue.put(("end_of_song", None))

    # Registra o evento de término da música.
    @player.event
    def on_eos():
        # Evento disparado pelo pyglet quando a música termina.
        notify_end_of_song()

    def update_audio_state(dt):
        """
            Envia periodicamente o estado atual do Player para o processo principal.

            Esse estado será utilizado posteriormente para atualizar o PlayerState e a interface.
        """

        # A fonte pode ainda não existir imediatamente após o carregamento de uma música.
        duration: float = (
            player.source.duration
            if player.source is not None else 0.0
        )

        state_queue.put({
            "position" : player.time,
            "duration" : duration,
            "is_playling" : player.playing,
            "volume" : player.volume
        })

    def process_commands(dt):
        """
        _summary_: 

        Args:
            dt (_type_): _description_
        """

        nonlocal player, volume

        # Processa todos os comandos que estiverem aguardando.
        while not command_queue.empty():

            """
                Cada comando possui:
                    ("nome_do_comando", valor)
                
                    Exemplos:
                        ("play", None)
                        ("pause", None)
                        ("volume", 0.5)
                        ("seek", 60)
                        ("load", "C:/musica.mp3")
            """
            command, value = command_queue.get()

            match command:

                case "load":
                    # Para a reprodução atual antes de tocar a música.
                    player.pause()
                    # Remove o Player atual.
                    player.delete()
                    # Cria um novo Player para a nova música.
                    player = pyg.media.Player()

                    player.volume = volume

                    # Registra novamente o evento de término no novo Player.
                    @player.event
                    def on_eos():
                        notify_end_of_song()

                    # converte o caminho da música em um Source do pyglet.
                    source = pyg.media.load(value)

                    # Coloca a música na fila interna do pyglet.
                    player.queue(source)

                case "play":
                    # Inicia ou continua a reprodução.
                    player.play()

                case "pause":
                    # Pausa a reprodução atual.
                    player.pause()

                case "volume":
                    # O volume é recebido pelo processo principal através do comando.
                    volume = value
                    player.volume = volume

                case "seek":
                    # Altera a posição atual da música.
                    # value representa a posição em segundos.
                    player.seek(value)
    
    # Verifica os comandos enviados pelo processo principal a cada 0.01 segundo.
    pyg.clock.schedule_interval(process_commands, 0.01)

    # Envia o estado atual do áudio a cada 0.1 segundo.
    pyg.clock.schedule_interval(update_audio_state, 0.1)

    # Inicia o Event Loop do pyglet.
    # Este é o Event Loop do processo de áudio, não o Event Loop da aplicação Flet.
    pyg.app.run()


class AudioProcess:

    # Process: Criação do processo separado.
    # Referência para o processo responsável pelo áudio.
    # Este objeto existe no processo principal.
    _process: Process | None = None

    # Queue: canal de comunicação.
    """
        Canal usado para enviar comandos:
            Processo principal
                ↓
            command_queue
                ↓
            Processo de áudio
    """
    _command_queue: Queue = None

    """
        Canal usado para receber eventos:
            Processo de áudio
                ↓
            event_queue
                ↓
            Processo principal
    """
    _event_queue: Queue = None

    """
        Comunicação:
            Processo de áudio
                ↓
            state_queue
                ↓
            Processo principal
    """
    _state_queue: Queue = None

    # Estado mais recente recebido do processo de áudio.
    _audio_state: dict[str, float | bool] = _AUDIO_STATE.copy()


    @classmethod
    def start(cls):
        """
        _summary_: Inicializa o processo independente de áudio.
        """

        # Impede que mais de um processo de áudio seja criado.
        if cls._process is not None:
            return

        # Criação do canal: Processo principal --> command_queue --> Processo de Áudio.
        # Cria a fila utilizada para enviar comandos ao processo de áudio. 
        cls._command_queue = Queue()

        # Cria a fila utilizada para receber eventos do processo de áudio.
        cls._event_queue = Queue()

        # Cria a fila utilizada para receber o estado atual do Player.
        cls._state_queue = Queue()

        # Cria o processo separado.
        # _run_audio_process será executado dentro dele.
        cls._process = Process(
            target = _run_audio_process,
            args = (
                cls._command_queue, 
                cls._event_queue, 
                cls._state_queue
            ),
            daemon = True
        )

        # Inicia efetivamente o processo.
        cls._process.start()

    @classmethod
    def send_command(cls, command: str, value = None):
        """
        Envia um comando para o processo de áudio.

        Exemplos:

            AudioProcess.send_command("play")

            AudioProcess.send_command("pause")

            AudioProcess.send_command(
                "volume",
                0.5
            )

            AudioProcess.send_command(
                "load",
                song_path
            )
        """

        # O processo ainda não foi iniciado.
        if cls._command_queue is None:
            return

        # Coloca o comando na fila.
        # O processo de áudio irá recebê-lo através de process_commands().
        cls._command_queue.put((command, value))

    @classmethod
    def get_event(cls) -> tuple | None:
        """
        _summary_: Obtém um evento enviado pelo processo de áudio.

        Returns:
            tuple | None: ...
        """

        # O processo ainda não foi iniciado.
        if cls._event_queue is None:
            return None

        # Não existe nenhum evento aguardado.
        # Não utilizamos .get() diretamente porque ele poderia bloquear esperando um evento.
        if cls._event_queue.empty():
            return None

        # Retorna o próximo evento.
        return cls._event_queue.get()

    @classmethod
    def get_state(cls) -> dict | None:
        """
        _summary_: Obtém um estado enviado pelo processo de áudio

        Returns:
            dict | None: ...
        """

        if cls._state_queue is None:
            return None

        if cls._state_queue.empty():
            return None

        return cls._state_queue.get()

    @classmethod
    def update_state(cls):
        """
            Atualiza o estado local utilizando o último estado enviado pelo processo de áudio.
        """

        if cls._state_queue is None:
            return

        while not cls._state_queue.empty():
            state = cls._state_queue.get()
            cls._audio_state.update(state)


    # getters
    @classmethod
    def get_position(cls) -> float:
        return cls._audio_state["position"]

    @classmethod
    def get_duration(cls) -> float:
        return cls._audio_state["duration"]

    @classmethod
    def is_playling(cls) -> bool:
        return cls._audio_state["is_playing"]

    @classmethod
    def get_volume(cls) -> float:
        return cls._audio_state["volume"]


    @classmethod
    def process_events(cls) -> list:
        """
            Processa os eventos enviados pelo processo de áudio.
            Retorna uma lista com os eventos recebidos.
        """

        events: list = []

        if cls._event_queue is None:
            return events

        while not cls._event_queue.empty():
            events.append(cls._event_queue.get())

        return events