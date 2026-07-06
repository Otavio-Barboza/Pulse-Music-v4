from abc import ABC, abstractmethod
# ABC (Abstract Base Class)

# classe não instanciável. Serve como modelo obrigatório. Evita de cada fonte retorna um JSON diferente e o resto do sistema quebra
class FonteMetadados(ABC):
    @abstractmethod
    async def buscar_musica(self, titulo : str, artista : str | None = None):
        pass

    @abstractmethod
    async def buscar_album(self, album_id : int):
        pass

    @abstractmethod
    async def buscar_artista(self, artista_id : int):
        pass