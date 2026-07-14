# import geral
from abc import ABC, abstractmethod
# ABC (Abstract Base Class)


# classe não instanciável. Serve como modelo obrigatório. Evita de cada fonte retorna um JSON diferente e o resto do sistema quebra
class MetadataSource(ABC):
    @abstractmethod
    async def get_song(self, title: str, artist: str | None = None):
        pass

    @abstractmethod
    async def get_album(self, id: str):
        pass

    @abstractmethod
    async def get_artist(self, id: str):
        pass