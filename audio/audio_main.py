# imports gerais
from pathlib import Path
from multiprocessing.connection import Listener
import threading, time, pyglet


PIPE_NAME = r"\\.\pipe\pulse_music_audio"


class AudioPlayer:

    def __init__(self):
        # Player do pyglet. Este objeto existe SOMENTE
        # dentro do processo audio_main.exe.
        self.player = pyglet.media.Player()

        # Música atualmente carregada.
        self.current_path: Path | None = None

        # Indica se a música já foi finalizada.
        # É utilizado pelo monitor para garantir que "song_finished" seja enviado apenas uma vez.
        self.finished: bool = False

        # Duração da música atualmente carregada.
        self.duration: float = 0


    def load(self, path: str):
        """
            Carrega uma nova música no player do pyglet.
        """

        path = Path(path)

        if not path.exists():
            print(f"[AUDIO] Arquivo não encontrado: {path}")
            return False

        # Interrompe qualquer reprodução anterior.
        self.stop()

        # Cria um novo Player para garantir que o estado anterior do pyglet não seja reaproveitado.
        self.player = pyglet.media.Player()

        source = pyglet.media.load(
            str(path),
            streaming = False
        )

        self.player.queue(source)

        self.current_path = path
        self.duration = source.duration

        # Uma nova música ainda não terminou
        self.finished = False

        print(f"[AUDIO] Música carregada: {path}")
        print(f"[AUDIO] Duração: {self.duration:.2f}s")

        return True

    def play(self):
        self.finished = False
        self.player.play()
        print("[AUDIO] PLAY")

    def pause(self):
        self.player.pause()
        print("[AUDIO] PAUSE")

    def stop(self):
        """
            Interrompe a reprodução e retorna para o início.

            O estado finished é marcado como True porque stop() não representa o término natural da música.
        """
        self.finished = True

        self.player.pause()

        try:
            self.player.seek(0)
        except Exception:
            pass

        print("[AUDIO] STOP")

    def set_volume(self, volume: float):
        self.player.volume = volume
        print(f"[AUDIO] VOLUME: {volume}")

    def seek(self, position: float):
        self.player.seek(position)
        print(f"[AUDIO] SEEK: {position:.2f}s")

    def get_position(self) -> float:
        return self.player.time

    def get_duration(self) -> float:
        return self.duration


class AudioServer:

    def __init__(self, audio_player: AudioPlayer):

        self.audio_player = audio_player

        self.listener = None
        self.connection = None

        self.running = True

        self.monitor_thread: threading.Thread | None = None

        # O monitor e a thread principal podem enviar eventos simultaneamente pelo mesmo Named Pipe.
        # O lock garante que cada mensagem seja enviada integralmente antes de outra thread utilizar a conexão.
        self.send_lock = threading.Lock()

    def start(self):

        print("[AUDIO] Iniciando servidor...")

        self.listener = Listener(
            PIPE_NAME,
            family = "AF_PIPE"
        )

        print("[AUDIO] Aguardando conexão...")

        self.connection = self.listener.accept()

        print("[AUDIO] Processo principal conectado.")

        self.start_monitor()

        self.run()

    def run(self):

        while self.running:

            try:

                if not self.connection.poll(0.1):
                    continue

                command = self.connection.recv()

                if not isinstance(command, dict):
                    continue

                self.process_command(command)

            except (
                BrokenPipeError, 
                EOFError, 
                OSError
            ):
                print("[AUDIO] Processo principal encerrado.")
                self.running = False

    def process_command(self, command: dict):

        action = command.get("action")

        match action:

            case "load":

                path = command.get("path")

                if not path:
                    return

                loaded = self.audio_player.load(path)

                # Só informa que a música foi carregada quando o carregamento realmente aconteceu.
                if loaded:
                    self.send_event(
                        event = "loaded",
                        data = {
                            "path" : path,
                            "duration" : (
                                self.audio_player.get_duration()
                            )
                        }
                    )

            case "play":
                self.audio_player.play()
                self.send_event("playing")

            case "pause":
                self.audio_player.pause()
                self.send_event("paused")

            case "stop":
                self.audio_player.stop()
                self.send_event("stopped")

            case "volume":

                volume = command.get("value")
                print(f"[AUDIO] Volume recebido: {volume}")
                if volume is None:
                    return

                self.audio_player.set_volume(volume)

                # Matemos o protocolo simples: o comando foi executado, então o estado local pode ser atualizado pelo processo principal.
                self.send_event(
                    event = "volume",
                    data = {
                        "volume" : volume
                    }
                )

            case "seek":

                position = command.get("position", 0.0)

                self.audio_player.seek(position)

                self.send_event(
                    event = "seekend",
                    data = {
                        "position" : position
                    }
                )

            case "shutdown":
                self.running = False
                print("[AUDIO] Encerrando...")

    def start_monitor(self):

        self.monitor_thread = threading.Thread(
            target = self.monitor,
            daemon = True
        )
        self.monitor_thread.start()

    def monitor(self):

        last_position = -1.0

        while self.running:

            time.sleep(0.1)

            position = self.audio_player.get_position()
            duration = self.audio_player.get_duration()

            # Não existe música carregada.
            if duration <= 0:
                continue

            # A música já foi marcada como finalizada. Isso evita que song_finished seja enviado várias vezes.
            if self.audio_player.finished:
                continue

            # Detecta o final da música.
            # Não dependemos de pyglet.on_eos. O monitor trabalha comparando a posição atual com a duração conhecida da música.
            if position >= duration - 0.1:

                self.audio_player.finished = True

                print("[AUDIO] Música terminou")
                
                self.send_event(
                    event = "position",
                    data = {
                        "position" : duration
                    }
                )

                self.send_event("song_finished")

                continue

            # Envia atualizações somente quando a posição realmente mudou.
            if position != last_position:

                last_position = position

                self.send_event(
                    event = "position",
                    data = {
                        "position" : position
                    }
                )

    def send_event(
        self,
        event: str,
        data: dict | None = None
    ):
        """
            Envia um evento para o processo principal.

            Tanto process_command() quanto monitor() podem chamar este método. Por isso utilizamos um Lock.
        """

        if not self.connection:
            return

        message = {
            "type": "event",
            "event": event,
            "data": data or {}
        }

        try:
            with self.send_lock:
                self.connection.send(message)
        except (
            BrokenPipeError, 
            EOFError,
            OSError
        ):
            self.running = False

    def close(self):

        self.running = False

        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass

            self.connection = None

        if self.listener:
            try:
                self.listener.close()
            except Exception:
                pass

            self.listener = None

        if self.monitor_thread:
            self.monitor_thread.join(
                timeout = 1
            )


def main():

    audio_player = AudioPlayer()

    server = AudioServer(audio_player)

    try:
        server.start()
    finally:
        server.close()


if __name__ == "__main__":
    main()