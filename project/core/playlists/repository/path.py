# import do colors
from ui.others.colors import color

# import de back-end
from core.services.account_manager import AccountManager

# imports gerais
from pathlib import Path
import os, datetime, shutil


class CreatePlaylist:

    @classmethod
    def generate_id(cls, dados: dict) -> str:
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
    def generate_date(cls) -> str:
        """
            Gera a data atual de cada execução para aplicar o ultimo momento de att ou o da criacão
        Returns:
            str: data formatada em string
        """
        return datetime.datetime.now().isoformat()
    
    @classmethod
    def count_number_of_songs(cls, path: Path) -> int:
        """
            Função para contar a quantidade de musicas contidas na pasta selecionada de músicas da playlist
        Args:
            path (str): path da pasta com as músicas

        Returns:
            int: retorna 0 (caso não exista a pasta) ou um N° int da quantidade na pasta.
        """
        if not path.exists():
            return 0

        return len([
            f for f in os.listdir(path)
            if f.lower().endswith((".mp3", ".wav", ".flac"))
        ])
    
    @classmethod
    def return_content_data_playlits(
        cls, 
        id: str,
        music_path: str,
        name : str,
        # origem_mus : str = 'pasta',
        image_path: Path,
        color : str = "#3d3d3d",
        opacity : float = 1.0,
        number_of_songs: int = 0
    ) -> dict:
        """
            Função para agilizar o retorno correto e formatado do conteudo do config_play.json
        Args:
            id (str): ID da playlist
            music_path (str): pasta com as músicas
            name (str): name da playlist
            image_path (str, optional): Caminho da imagem da playlist (Album ou Capa de Música). Defaults to r'Assets/Global/Images/Padrao/capa_playlist_padrao.png'.
            color (str, optional): Cor de fundo da playlist (com opacity). Defaults to "#3d3d3d".
            opacity (float, optional): Opacidade salva separadamente. Defaults to 1.0.
            number_of_songs (int, optional): Quantidade de músicas. Defaults to 0.

        Returns:
            dict: Dicionário formatado com todos os elementos pronto para salvar no JSON.
        """
        date: str = cls.generate_date()

        return {
            "id" : id,
            "name" : name,

            "style" : {
                "image_path" : image_path,
                "color" : color,
                "opacity" : opacity
            },

            "music" : {
                # "origem" : origem_mus,
                "music_path" : music_path,
                "number_of_songs" : number_of_songs
            },

            "date" : {
                "creation_date": date,
                "latest_actualization": date
            }
        }

    @classmethod
    def return_name_playlist_json(cls, name : str) -> str:
        """
            Retorna a instancia da nova playlist para adicionar ao playlist.json
        Args:
            name (str): Nome da Playlist

        Returns:
            str: nome.
        """
        return name

    @classmethod
    def return_selection_images(cls) -> list[str] | list[str] | tuple[str, str]:
        """
            Função para retornar as imagens dos Álbuns e Capas de Músicas para os métodos CREATE e UPDATE das playlists.
        Returns:
            list[str] | tuple[str, str]: duas listas (listagem das imagens) e uma tupla (caminho de cada pasta)
        """
        return os.listdir(
            f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Imagens/Albuns'
        ), os.listdir(
            f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Imagens/Capa Musica'
        ), tuple(
            f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Imagens/Albuns', 
            f'Assets/Data/Contas/{AccountManager.account_cache["current_account"]}/Imagens/Capa Musica'
        )
    
    @classmethod
    def remove_path(cls, path: Path):
        """
            Remove a path da playlist + o JSON config_play
        Args:
            path (Path): caminho da path da playlist
        """
        path: Path = Path(path)

        if path.exists() and path.is_dir():
            shutil.rmtree(path)