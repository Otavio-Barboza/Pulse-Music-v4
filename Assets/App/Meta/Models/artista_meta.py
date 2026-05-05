class MusicasArtistas:
    def __init__(self):
        self.artistas: dict = {}

    def adicionar_musica(
        self,
        caminho_completo: str,
        # artista_id: str | None,
        nome: str | None
    ):
        from ...Meta.Repository.normalizacao import Filtragem

        if not nome:
            return  
        
        nome_base = Filtragem.artista_base(nome)

        if nome_base not in self.artistas:
            self.artistas[nome_base] = {
                'nome' : nome,
                'musicas': []
            }

        self.artistas[nome_base]["musicas"].append(caminho_completo)

    def remover(self, track_id: str, artista_id: str | None):
        if not artista_id:
            return

        if artista_id not in self.artistas:
            return

        lista = self.artistas[artista_id]["musicas"]

        if track_id in lista:
            lista.remove(track_id)

        if not lista:
            del self.artistas[artista_id]

    def to_dict(self):
        return self.artistas