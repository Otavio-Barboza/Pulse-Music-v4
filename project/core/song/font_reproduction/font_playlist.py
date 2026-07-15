# imports de back-end
from core.song.font_reproduction.font_reproduction import ReproductionFont
from core.song.repository.song_repository import SongRepository
from core.song.model.reproduction import Reproduction
from core.song.enum.song_enum import ReproductionMode

# import geral
from pathlib import Path


class PlaylistFont(ReproductionFont):

    def __init__(self, mode: ReproductionMode, path: Path):
        self.mode = mode
        self.path = path
    
    def carregar(self) -> list:
        return SongRepository.load_songs(
            path = self.path,
            mode = self.mode
        )
    
    def carregar_playlist(self, lista_musicas):
        Reproduction.load_songs_from_mode(
            mode = self.mode, 
            list = lista_musicas
        )