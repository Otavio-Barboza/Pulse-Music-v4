import os, uuid

class RepositorioMusica:
    @classmethod
    def gerar_id(cls) -> str:
        return str(uuid.uuid4())
    
    @classmethod
    def _carregar_musicas(cls, pasta : str) -> list[Musica]:
        return [
            Musica(
                nome = m.replace('.mp3', ''),
                caminho = os.path.join(pasta, m),
                id = cls.gerar_id()
            ) for m in os.listdir(pasta)
        ]