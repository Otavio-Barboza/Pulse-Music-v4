from abc import ABC, abstractmethod
from typing import List
from ...Music.Model.musica import Musica
from ...Music.Repository.musica_repositorio import RepositorioMusica

class FonteMusica(ABC):
    @abstractmethod
    def carregar(self) -> List[Musica]:
        pass