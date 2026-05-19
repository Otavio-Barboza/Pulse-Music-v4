from abc import ABC, abstractmethod
from typing import List
from ..Repository.musica_repositorio import RepositorioMusica

class FonteReproducao(ABC):
    @abstractmethod
    def carregar(self) -> List:
        pass