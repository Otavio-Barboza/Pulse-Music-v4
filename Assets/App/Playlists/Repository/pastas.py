from ...Services.gerenciador_contas import GerenciadorContas
from ....Interface.Others.cores import cor
import os, json, datetime, shutil, pathlib

class CreatePlaylist:
    @classmethod
    def ler_json(cls, caminho):
        with open(caminho, 'r', encoding = 'utf-8') as js:
            return json.load(js)
    
    @classmethod
    def escrever_json(cls, caminho : str, dados : dict):
        with open(caminho, 'w', encoding = 'utf-8') as js:
            json.dump(dados, js, indent = 4, ensure_ascii = False)
    
    @classmethod
    def criar_pasta(cls, path):
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def gerar_id(cls, dados) -> str:
        """
            Gera o ID novo com base no último salvo, funciona acrescentando +1 em sequencia.
        Args:
            dados (dict): dados do playlist.json

        Returns:
            str: Novo ID em string
        """
        id =  dados.get('ultimo_id') + 1

        if id < 10:
            return f'pl_00{id}', id
        elif id < 100:
            return f'pl_0{id}', id
        else:
            return f'pl_{id}', id
    
    @classmethod
    def gerar_data(cls) -> str:
        """
            Gera a data atual de cada execução para aplicar o ultimo momento de att ou o da criacão
        Returns:
            str: data formatada em string
        """
        return datetime.datetime.now().isoformat(timespec = 'seconds')
    
    @classmethod
    def contar_qtde_musicas(cls, caminho : str) -> int:
        """
            Função para contar a quantidade de musicas contidas na pasta selecionada de músicas da playlist
        Args:
            caminho (str): caminho da pasta com as músicas

        Returns:
            int: retorna 0 (caso não exista a pasta) ou um N° int da quantidade na pasta.
        """
        if not os.path.exists(caminho):
            return 0

        return len([
            f for f in os.listdir(caminho)
            if f.lower().endswith((".mp3", ".wav", ".flac"))
        ])
    
    @classmethod
    def retornar_conteudo_config_play_json(
        cls, 
        id : str,
        pasta_mus : str,
        nome : str,
        origem_mus : str = 'pasta',
        pasta_img : str = r'Assets\Global\Images\Padrao\capa_playlist_padrao.png',
        cor : str = "#3d3d3d",
        opacidade : float = 1.0,
        qtde_mus : int = 0
    ) -> dict:
        """
            Função para agilizar o retorno correto e formatado do conteudo do config_play.json
        Args:
            id (str): ID da playlist
            pasta_mus (str): pasta com as músicas
            nome (str): nome da playlist
            origem_mus (str, optional): instancia que diferencia da playlist normal ('pasta') da coleção de musicas ('fav').
            pasta_img (str, optional): Caminho da imagem da playlist (Album ou Capa de Música). Defaults to r'Assets/Global/Images/Padrao/capa_playlist_padrao.png'.
            cor (str, optional): Cor de fundo da playlist (com opacidade). Defaults to "#3d3d3d".
            opacidade (float, optional): Opacidade salva separadamente. Defaults to 1.0.
            qtde_mus (int, optional): Quantidade de músicas. Defaults to 0.

        Returns:
            dict: Dicionário formatado com todos os elementos pronto para salvar no JSON.
        """
        data = cls.gerar_data()

        return {
            "id" : id,
            "nome" : nome,

            "style" : {
                "pasta" : pasta_img,
                "cor" : cor,
                "opacidade" : opacidade
            },

            "musicas" : {
                "origem" : origem_mus,
                "pasta" : pasta_mus,
                "quantidade_de_musicas" : qtde_mus
            },

            "datas" : {
                "criado_em": data,
                "ultima_atualizacao": data
            }
        }

    @classmethod
    def retornar_conteudo_playlist_json(
        cls, 
        nome : str,
        tipo : str
    ) -> dict:
        """
            Retorna a instancia da nova playlist para adicionar ao playlist.json
        Args:
            nome (str): Nome da Playlist
            tipo (str): Tipo dela (pasta ou fav)

        Returns:
            dict: Dicionário pronto para salvar no JSON
        """
        return {
            "nome" : nome,
            "tipo" : tipo
        }

    @classmethod
    def _retornar_imagens_selecao(cls) -> list[str] | tuple[str, str]:
        """
            Função para retornar as imagens dos Álbuns e Capas de Músicas para os métodos CREATE e UPDATE das playlists.
        Returns:
            list[str] | tuple[str, str]: duas listas (listagem das imagens) e uma tupla (caminho de cada pasta)
        """
        usuario = GerenciadorContas.contas_cache
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{usuario["conta_atual"]}/Imagens/Albuns'
        CAMINHO_CAPAS = f'Assets/Data/Contas/{usuario["conta_atual"]}/Imagens/Capa Musica'
        return os.listdir(CAMINHO_ALBUNS), os.listdir(CAMINHO_CAPAS), (CAMINHO_ALBUNS, CAMINHO_CAPAS)
    
    @classmethod
    def remover_pasta(cls, pasta : str):
        """
            Remove a pasta da playlist + o JSON config_play
        Args:
            pasta (str): caminho da pasta da playlist
        """
        path = pathlib.Path(pasta)

        if path.exists() and path.is_dir():
            shutil.rmtree(path)