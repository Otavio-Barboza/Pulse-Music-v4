from ..Model.musica import Musica
from ...Meta.Repository.tarefas import GerenciaMetadados
import os

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

    @classmethod
    def buscar_artista(cls, chave_musica : str):
        from ...Services.gerenciador_contas import GerenciadorContas
        import json
        
        with open(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json', 
            'r', 
            encoding = 'utf-8'
        ) as js:
            json_musicas = json.load(js)
            
        for chave, item in json_musicas.items():
            if chave == chave_musica:
                artista = item.get('artista_final')
                return artista if artista is not None else 'Artista Desconhecido'
            
    @classmethod
    def buscar_capa(cls, musica : str):
        from ...Services.gerenciador_contas import GerenciadorContas
        
        for capa in os.listdir(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Capa Musica'
        ):
            if capa.removesuffix('.jpg') == musica:
                return os.path.normpath(
                    os.path.join(
                        f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Capa Musica',
                        capa
                    )
                )
        else:
            return r'Assets\Global\Images\Padrao\capa_musicas_desconhecidas.png'
    
    @classmethod
    def buscar_musica(cls, chave_musica : str):
        from ...Services.gerenciador_contas import GerenciadorContas
        import json
        
        with open(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json', 
            'r', 
            encoding = 'utf-8'
        ) as js:
            json_musicas = json.load(js)
        
        for chave, item in json_musicas.items():
            if chave == chave_musica:
                musica = item
                break

        if musica['nome_musica_filtrado'].get('titulo_ID3_filtrado') is not None:
            return musica['nome_musica_filtrado'].get('titulo_ID3_filtrado')
        elif musica['nome_musica_filtrado'].get('arquivo_mp3_filtrado') is not None:
            return musica['nome_musica_filtrado'].get('arquivo_mp3_filtrado')
        elif musica['titulo_ID3_original'] is not None:
            return musica.get('titulo_ID3_original')
        else:
            return musica.get('arquivo_original')