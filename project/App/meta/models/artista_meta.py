class MusicasArtistas:
    def __init__(self):
        self.artistas: dict[str, list[dict[str]]] = {}

    def adicionar_musica(
        self,
        chave_musica: str,
        caminho_chave_musica : str ,
        artista_id: str | None,
        nome_artista_final : str
    ):

        if not artista_id or not chave_musica:
            return  
        
        if artista_id not in self.artistas:
            self.artistas[artista_id] = {
                'nome_artistas' : nome_artista_final,
                'musicas': []
            }

        self.artistas[artista_id]["musicas"].append({
            'chave' : chave_musica, 
            'caminho_completo' : caminho_chave_musica
        })

    # def remover(self, track_id: str, artista_id: str | None):
    #     if not artista_id:
    #         return

    #     if artista_id not in self.artistas:
    #         return

    #     lista = self.artistas[artista_id]["musicas"]

    #     if track_id in lista:
    #         lista.remove(track_id)

    #     if not lista:
    #         del self.artistas[artista_id]

    def to_dict(self):
        return self.artistas