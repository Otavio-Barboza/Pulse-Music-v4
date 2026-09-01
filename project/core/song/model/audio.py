# imports gerais
from pathlib import Path
from multiprocessing.connection import Client
import subprocess, sys, threading, time


_AUDIO_STATE: dict[str, float | bool | None] = {
    "position" : 0.0,
    "duration" : 0.0,
    "is_playing" : False,
    "volume" : 1.0
}


class AudioProcess:

    PIPE_NAME: str = r"\\.\pipe\pulse_music_audio"

    # Representa o processo externo: audio_main.exe
    _process: subprocess.Popen | None = None

    #  Representa a conexão: Pulse Music ←→ Named Pipe ←→ audio_main.exe
    _connection = None

    # Controle da thread responsável por receber eventos.
    _running: bool = False
    
    # Fica continuamente esperando mensagens do processo de áudio.
    _listener_thread: threading.Thread | None = None

    # Estado conhecido pelo processo principal.
    _audio_state = _AUDIO_STATE.copy()

    # Callbacks de eventos recebidos do processo de áudio.
    # Estes callbacks NÃO são callbacks de interface.
    # Servem apenas para entregar eventos do AudioProcess para a camada que gerencia a reprodução.
    _event_callbacks: dict[str, list[callable]] = {}


    @classmethod
    def get_audio_executable(cls) -> Path:
        """
            Localiza o executável responsável pelo áudio.
        """

        if getattr(sys, "frozen", False):
            return (
                Path(sys.executable).parent / "audio_main.exe"
            )

        return (
            Path(__file__).resolve().parents[3] / "assets" / "app" / "audio_main.exe"
        )


    # EVENTOS

    @classmethod
    def register_event_callback(
        cls,
        event: str,
        callback: callable
    ):
        """
            Registra um callback para um evento enviado
            pelo audio_main.exe.

            Exemplo:

                AudioProcess.register_event_callback(
                    "song_finished",
                    callback
                )
        """
        cls._event_callbacks.setdefault(
            event, []
        ).append(callback)

    @classmethod
    def notify_event(
        cls,
        event: str,
        data: dict
    ):
        """
            Notifica os callbacks registrados para determinado evento.

            O AudioProcess não toma decisões sobre a reprodução.
            Ele apenas repassa a informação recebida.
        """

        for callback in cls._event_callbacks.get(event, []):

            try:
                callback(data)
                print(f"[AUDIO PROCESS] Notificando: {event}")
            except Exception as error:
                print(
                    f"[AUDIO PROCESS] "
                    f"Erro no callback '{event}': {error}"
                )


    # PROCESSO

    @classmethod
    def start(cls):
        """
            Inicia o audio_main.exe, conecta ao Named Pipe e inicia a thread de recebimento dos eventos.
        """

        if cls._process is not None:
            return

        # Tenta encontrar o audio_main.exe
        audio_executable: Path = cls.get_audio_executable()

        # caso não encontre o audio_main.exe
        if not audio_executable.exists():
            raise FileNotFoundError(
                f"Executável de áudio não encontrado: "
                f"{audio_executable}"
            )

        print("[MAIN] Iniciando processo de áudio...")

        # Chamada do Popen
        cls._process = subprocess.Popen(
            [str(audio_executable)]
        )

        # Conecta ao Named Pipe
        cls.connect()

        # Inicia o listener
        cls.start_listener()

    @classmethod
    def connect(cls):
        """
            Tenta estabelecer a conexão com o Named Pipe criado pelo audio_main.exe.
        """

        for _ in range(50):

            try:
                cls._connection = Client(
                    cls.PIPE_NAME,
                    family = "AF_PIPE"
                )

                print("[MAIN] Conectado ao processo de áudio.")

                return

            except Exception:
                time.sleep(0.1)

        raise RuntimeError(
            "Não foi possível conectar ao processo de áudio."
        )

    @classmethod
    def start_listener(cls):
        """
            Cria a thread que ficará responsável por receber eventos do processo de áudio.
        """

        if cls._running:
            return

        cls._running = True

        cls._listener_thread = threading.Thread(
            target = cls.listen,
            daemon = True
        )

        cls._listener_thread.start()

    @classmethod
    def listen(cls):
        """
            Escuta continuamente o Named Pipe.

            Esta função roda em uma thread separada, portanto não bloqueia o processo principal/Flet.
        """

        while cls._running:

            try: 
                if not cls._connection.poll(0.1):
                    continue 

                message = cls._connection.recv()

                if not isinstance(message, dict):
                    continue

                cls.process_event(message)
            except (
                BrokenPipeError,
                EOFError,
                OSError
            ):
                cls._running = False
                break

    @classmethod
    def process_event(cls, message: dict):
        """
            Processa uma mensagem recebida do audio_main.exe.

            Aqui existem duas responsabilidades:

            1. Atualizar o estado local do áudio.
            2. Propagar eventos importantes para a camada
            de gerenciamento da reprodução.
        """

        if message.get("type") != "event":
            return

        event: str = message.get("event")
        data: dict = message.get("data", {})

        print(f"[AUDIO PROCESS] Evento recebido: {event} | {data}")

        match event:

            case "loaded":
                cls._audio_state["duration"] = (
                    data.get("duration", 0.0)
                )
                cls._audio_state["position"] = 0.0

            case "playing":
                cls._audio_state["is_playing"] = True

            case "paused":
                cls._audio_state["is_playing"] = False

            case "stopped":
                cls._audio_state["is_playing"] = False
                cls._audio_state["position"] = 0.0

            case "seeked":
                cls._audio_state["position"] = (
                    data.get("position", 0.0)
                )

            case "position":
                cls._audio_state["position"] = (
                    data.get("position", 0.0)
                )

            case "volume":
                cls._audio_state["volume"] = (
                    data.get(
                        "volume", 
                        cls._audio_state["volume"]
                    )
                )

            case "song_finished":
                # A música terminou no processo de áudio.
                cls._audio_state["is_playing"] = False

        cls.notify_event(event = event, data = data)


    # COMANDOS

    @classmethod
    def send_command(
        cls,
        action: str,
        value = None
    ):
        """
            Envia comandos para o audio_main.exe. 
            O formato dos dados depende da ação.
        """

        if cls._connection is None:
            return

        # O protocolo do audio_main possui campos diferentes dependendo do comando.
        
        match action:

            case "load":
                command = {
                    "action" : "load",
                    "path" : value
                }

            case "volume":
                command = {
                    "action" : "volume",
                    "value" : value
                }

            case "seek":
                command = {
                    "action" : "seek",
                    "position" : value
                }

            case _:
                command = {
                    "action" : action
                }

        try:
            cls._connection.send(command)
        except (
            BrokenPipeError,
            EOFError,
            OSError
        ):
            cls._running = False


    # GETTERS | ESTADO

    @classmethod
    def get_position(cls) -> float:
        return cls._audio_state["position"]

    @classmethod
    def get_duration(cls) -> float:
        return cls._audio_state["duration"]

    @classmethod
    def is_playing(cls) -> bool:
        return cls._audio_state["is_playing"]

    @classmethod
    def get_volume(cls) -> float:
        return cls._audio_state["volume"]

    @classmethod
    def get_audio_state(cls) -> dict:
        return cls._audio_state.copy()


    # Comandos públicos
    @classmethod
    def load(cls, path: str):
        cls.send_command("load", path)

    @classmethod
    def play(cls):
        cls.send_command("play")

    @classmethod
    def pause(cls):
        cls.send_command("stop")

    @classmethod
    def seek(cls, position: float):
        cls.send_command("seek", position)

    @classmethod
    def set_volume(cls, volume: float):

        volume = max(
            0.0, min(1.0, volume)
        )

        cls._audio_state["volume"] = volume

        cls.send_command("volume", volume)


    # ENCERRAMENTO

    @classmethod
    def shutdown(cls):
        """
            Encerra corretamente a comunicação e o processo externo de áudio.
        """

        cls._running = False

        if cls._connection:
            
            try:
                cls.send_command("shutdown")
            except Exception:
                pass

        if cls._listener_thread:
            cls._listener_thread.join(timeout = 1)

        if cls._connection:

            try:
                cls._connection.close()
            except Exception:
                pass

            cls._connection = None

        if cls._process:

            try:
                cls._process.wait(timeout = 5)
            except subprocess.TimeoutExpired:
                cls._process.kill()

            cls._process = None