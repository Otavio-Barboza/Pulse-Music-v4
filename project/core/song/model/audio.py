# import de back-end
from core.song.model.monitoring import Monitoring

# imports gerais
from multiprocessing import Process, Queue
import pyglet as pyg


def _run_audio_process(command_queue: Queue, event_queue: Queue):
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
    """

    player = pyg.media.Player()

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
        notify_end_of_song()

    def process_commands(dt):
        """
        _summary_: 

        Args:
            dt (_type_): _description_
        """
        nonlocal player

        # Processa todos os comandos que estiverem aguardando.
        while not command_queue.empty():

            """
                Cada comando possui:
                    ("nome_do_comando", valor)
                
                    Exemplos:
                        ("play", None)
                        ("volume", 0.5)
                        ("load", "C:/music.mp3")
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

                    # Registra novamente o evento de término no novo Player.
                    @player.event
                    def on_eos():
                        event_queue.put(("end_of_song", None))

                    # Coloca a música na fila interna do pyglet.
                    player.queue(value)

                case "play":
                    # Inicia ou continua a reprodução.
                    player.play()

                case "pause":
                    # Pausa a reprodução atual.
                    player.pause()

                case "volume":
                    # O volume é recebido pelo processo principal através do comando.
                    player.volume = value
    
    """
        Adicona process_commands ao Event Loop do pyglet.

        A cada 0.01 segundo, o pyglet verifica se existem novos comandos enviados pelo processo principal.
    """
    pyg.clock.schedule_interval(process_commands, 0.01)

    """
        Inicia o Event Loop do pyglet.

        IMPORTANTE:
            Este código está sendo executado na thread principal do processo de áudio, não na thread principal do flet.
    """
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
    _command_queue: Queue | None = None

    """
        Canal usado para receber eventos:
        
            Processo de áudio
                ↓
            event_queue
                ↓
            Processo principal
    """
    _event_queue: Queue | None

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

        # Cria o processo separado.
        # _run_audio_process será executado dentro dele.
        cls._process = Process(
            target = _run_audio_process,
            args = (cls._command_queue, cls._event_queue),
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