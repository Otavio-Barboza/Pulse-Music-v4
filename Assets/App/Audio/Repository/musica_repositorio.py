from ..Model.musica import Musica
from ...Meta.Repository.tarefas import GerenciaMetadados
import os, uuid

class RepositorioMusica:
    @classmethod
    def _carregar_musicas(cls, pasta, modo) -> list[Musica]:
        return [
            Musica(
                nome = m.removesuffix('.mp3'),
                caminho = os.path.normpath(
                    os.path.join(pasta, m)
                ),
                chave = GerenciaMetadados.gerar_track_id(
                    os.path.normpath(
                        os.path.join(pasta, m)
                    )
                ),
                modo = modo
            ) for m in os.listdir(pasta)
        ]
