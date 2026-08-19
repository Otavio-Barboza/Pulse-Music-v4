# import de back-end
from core.song.model.audio import AudioProcess

# imports gerais
from pathlib import Path


class Player:

    # Armazena o volume atual conhecido pelo processo principal.
    # O valor real será aplicado no pyglet.Player através do AudioProcess.
    _volume = 1.0


    @classmethod
    def load_song(cls, path: Path):
        """
        _summary_: (
            Solicita ao processo de áudio que carregue uma música.

            O Player não acessa mais o pyglet diretamente.
            Ele apenas envia o comando para o AudioProcess.
        )

        Args:
            path (Path): Caminho da música que deve ser carregada.
        """

        AudioProcess.send_command("load", str(path))

    @classmethod
    def play(cls):
        """
            Solicita ao processo de áudio que inicie ou continue a reprodução da música atual.
        """

        AudioProcess.send_command("play")

    @classmethod
    def pause(cls):
        """
            Solicita ao processo de áudio que pause a reprodução.
        """

        AudioProcess.send_command("pause")

    @classmethod
    def stop(cls):
        """
            Pausa a reprodução e retorna a posição para o início.
        """

        AudioProcess.send_command("pause")
        AudioProcess.send_command("seek", 0)
    
    @classmethod
    def formatted_total_duration(cls) -> str:
        """
            Retorna a duração total da música formatada como:

                MM:SS

            A obtenção da duração ainda será adaptada para funcionar através da comunicação com o processo de áudio.
        """

        font: float = cls.current_duration()
        
        minutes = int(font / 60)
        seconds = int(font - (minutes * 60))

        return f"{minutes:02}:{seconds:02}"

    @classmethod
    def formatted_current_duration(cls) -> str:
        """
            Retorna a posição atual da música formatada como:

                MM:SS

            A posição será obtida através do estado enviado pelo processo de áudio.
        """

        font: float = cls.current_position()
        
        minutes = int(font / 60)
        seconds = int(font - (minutes * 60))
        
        return f"{minutes:02}:{seconds:02}" or f"00:00"
    
    @classmethod
    def current_position(cls) -> float:
        """
            Retorna a posição atual conhecida da reprodução.
        """

        return AudioProcess.get_position()
    
    @classmethod
    def current_duration(cls) -> float:
        """
            Retorna a duração atual conhecida da música.
        """

        return AudioProcess.get_duration()

    @classmethod
    def set_volume(cls, volume: float):
        """
            Define o volume da reprodução.

            O valor é limitado ao intervalo aceito pelo pyglet:

                0.0 → mínimo
                1.0 → máximo

            Depois da validação, o valor é enviado para o processo de áudio.
        """

        cls._volume = max(0.0, min(1.0, volume))
        AudioProcess.send_command("volume", cls._volume)

    @classmethod
    def get_volume(cls):
        """
            Retorna o volume conhecido pelo processo principal.
        """

        return cls._volume

    @classmethod
    def go_to(cls, seconds: float):
        """
            Solicita ao processo de áudio que altere a posição atual da música.
        """
        AudioProcess.send_command("seek", seconds)