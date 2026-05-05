from .artista_meta import MusicasArtistas
from .albuns_meta import MusicasAlbuns

class MemoriaMetadados:
    def __init__(self):
        self.tracks: dict = {}
        self.artistas = MusicasArtistas()
        self.albuns = MusicasAlbuns()

    def carregar(self, dados_tracks: dict):
        self.tracks = dados_tracks
        self._reconstruir_indices()

    def _reconstruir_indices(self):
        import os

        self.artistas = MusicasArtistas()
        self.albuns = MusicasAlbuns()

        for track_id, dados in self.tracks.items():
            from pathlib import Path

            caminho_art = os.path.join(dados.get('caminho', ''), dados.get("arquivo_original", ""))
            self.artistas.adicionar_musica(
                nome = dados.get('artista_final'),
                caminho_completo = dados.get('artista', '').get('img_big', '').get('caminho', '') or caminho_art
            )

            caminho_alb = os.path.join(dados.get('caminho', ''), dados.get('arquivo_original', ''))
            self.albuns.adicionar_album(
                nome = dados.get('album').get('nome_album'),
                caminho_musica = dados.get('album').get('img_big').get('caminho') or caminho_alb
            )

    def atualizar_artista(
        self,
        track_id: str,
        novo_artista_id: str,
        novo_nome: str,
        nova_img: str
    ):
        track = self.tracks[track_id]

        artista_antigo = track["artista"]["id_artista_deezer"]

        track["artista"]["id_artista_deezer"] = novo_artista_id
        track["artista_final"] = novo_nome
        track["artista"]["img_big"] = nova_img

        self.artistas.remover(track_id, artista_antigo)
        self.artistas.adicionar_musica(
            track_id,
            novo_artista_id,
            novo_nome,
            nova_img
        )