# imports de back-end
from core.utils.utils import Utils
from core.services.account_manager import AccountManager
from core.playlists.models.playlist import Playlist
from core.playlists.models.playlist_config import PlaylistConfig
from core.playlists.models.playlist_card import PlaylistCard
from core.playlists.repository.path import CreatePlaylist
from core.utils.path import AppPaths

# imports gerais
from pathlib import Path
import os, asyncio


class PlaylistRepository:

    @classmethod
    def load_itens(cls) -> list[Playlist]:
        """
            Retorna uma lista com objetos Playlist() para auxiliar no carregamento das playlist ao rodar o app.
        Returns:
            list[Playlist]: lista com objetos Playlist().
        """
        
        set_playlists: set = set()
        playlists = Utils.sync_load_json(AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "playlists.json")

        for key, value in playlists.get("playlists").items():
            set_playlists.add(Playlist(
                id = key,
                name = value.get("name"),
                path = value.get("path")
            ))
        
        return list(set_playlists)
    
    @classmethod
    def load_cards(cls) -> list[PlaylistCard]:
        """
            Com auxílio do cls.carregar_itens utiliza-se dos objetos Playlist() e com eles carrega os detalhes de cada playlist, armazenando-os na lista cards os objetos PlaylistCard().
        Returns:
            list[PlaylistCard]: Lista com objetos PlaylistCard()
        """
        playlists: list[Playlist] = cls.load_itens()
        cards: set[PlaylistCard] = set()

        for playlist in playlists:
            playlist_config = Utils.sync_load_json(
                AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "playlists" / playlist.id / "config_play.json"
            )
            
            path = playlist_config["music"].get("music_path")
            qtde = CreatePlaylist.count_number_of_songs(Path(path))

            cards.add(PlaylistCard(
                id = playlist.id,
                name = playlist_config["name"],
                image_path = playlist_config["style"]["image_path"],
                color = playlist_config["style"]["color"],
                opacity = playlist_config["style"]["opacity"],
                playlist_path = path,
                number_of_songs = qtde
            ))
        
        return list(cards)
    
    @classmethod
    def list_playlists(cls) -> list[PlaylistCard]:
        """
            Chama cls.load_cards para intermediar o retorno das playlists ao EstadoPlaylist
        Returns:
            list[PlaylistCard]: lista com objetos PlaylistCard()
        """
        return cls.load_cards()
    
    @classmethod
    def count_number_of_songs(cls, path: str) -> int:
        """
            Intermédio para EstadoPlaylist e outras chamadas do contador da quantidade de músicas da playlist.
        Args:
            path (str): caminho da pasta

        Returns:
            int: N° int da quantidade de músicas da playlist
        """
        return CreatePlaylist.count_number_of_songs(Path(path))

    @classmethod
    def create_playlist(
        cls, 
        name : str, 
        music_path : str,
        image_path : str,
        color : str,
        opacity : float

    ) -> Playlist:
        """
            Cria o objeto Playlist, a pasta, json da playlist e adição ao json playlists da existencia da playlist nova
        Args:
            name (str): Nome da Plalist
            tipo (str): tipo (pasta ou fav)
            music_path (str): caminho da pasta das musicas
            origem_mus (str): origem das musicas (pasta ou dinamica das favoritas)
            image_path (str): caminho da imagem
            color (str): color do bgcolor do card
            opacity (float): valor da opacity da color

        Returns:
            Playlist: Objeto Playlist()
        """

        
        # Salvando dados do playlists.json
        dados = Utils.sync_load_json(
            path = AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "playlists.json"
        )

        new_id, id_num = CreatePlaylist.generate_id(data = dados)

        PASTA_PLAYLIST = AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "playlists" / new_id
        Utils.create_path(PASTA_PLAYLIST)

        dados["latest_id"] = id_num

        dados["playlists"][new_id] = {
            "name" : name,
            "path" : str(PASTA_PLAYLIST)
        }
        dados["latest_aztualization"] = CreatePlaylist.generate_date()

        Utils.sync_update_json(
            path = AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "playlists.json",
            data = dados
        )


        # salvando os dados do config_json
        qtde = CreatePlaylist.count_number_of_songs(Path(music_path))

        json_config = CreatePlaylist.return_content_data_playlits(
            id = new_id,
            music_path = music_path,
            image_path = image_path,
            color = color,
            opacity = opacity,
            name = name,
            number_of_songs = qtde
        )

        Utils.sync_update_json(
            path = AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "playlists" / new_id / "config_play.json",
            data = json_config
        )

        return Playlist(
            id = new_id,
            name = name,
            path = PASTA_PLAYLIST
        )

    @classmethod
    def return_images(cls) -> list[str] | tuple[str, str]:
        """
            Intermedio ao EstadoPlaylist para a listagem de imagens 
        Returns:
            list[str] | tuple[str, str]: Lista das imagens e tupla com os caminhos dos albuns e capas
        """
        return CreatePlaylist.return_selection_images()
    
    @classmethod
    def save_config(cls, playlist: PlaylistConfig):
        """
            Salva os dados do UPDATE da playlist em ambos JSONs
        Args:
            playlist (PlaylistConfig): Objeto PlaylistConfig para uso na inserção dos dados
        """
        usuario = AccountManager.accounts_cache
        caminho_config_json = f'Assets/Data/Contas/{usuario["current_account"]}/Playlists/{playlist.id}/config_play.json'
        caminho_play_json = f'Assets/Data/Contas/{usuario["current_account"]}/playlists.json'
 
        json_config = Utils.sync_load_json(caminho_config_json)
        json_play = Utils.sync_load_json(caminho_play_json)

        json_play['playlists'][playlist.id]['name'] = playlist.name
        json_play['latest_aztualization'] = CreatePlaylist.generate_date()

        json_config['name'] = playlist.name
        json_config['style']['pasta'] = playlist.style['path']
        json_config['style']['color'] = playlist.style['color']
        json_config['style']['opacity'] = playlist.style["opacity"]
        json_config['music']['path'] = playlist.music['path']
        json_config['music']['number_of_songs'] = CreatePlaylist.count_number_of_songs(playlist.music['pasta'])
        json_config['date']['latest_aztualization'] = CreatePlaylist.generate_date()

        Utils.sync_update_json(path = caminho_play_json, data = json_play)
        Utils.sync_update_json(path = caminho_config_json, data = json_config)
    
    @classmethod
    def remove_playlist_json(cls, id: str):
        """
            Remove a playlist do indice no JSON playlists
        Args:
            id (str): ID da playlist
        """
        usuario = AccountManager.accounts_cache
        caminho = f'Assets/Data/Contas/{usuario["current_account"]}/playlists.json'
        dados = Utils.sync_load_json(caminho)
        
        if id in dados['playlists']:
            dados['playlists'].pop(id)
            dados['latest_aztualization'] = CreatePlaylist.generate_date()
        
        Utils.sync_update_json(path = caminho, data = dados)
        

    @classmethod
    def delete_playlist(cls, id: str):
        """
            Função para executar a exclusão dos elementos da playlist
        Args:
            id (str): ID da Playlist
        """
        from core.meta.scanner.scanner import Scanner
        
        caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Playlists/{id}'
        leitura_json = Utils.sync_load_json(f'{caminho}/config_play.json')

        pasta = leitura_json.get('musicas').get('pasta')
        
        chaves_para_remover = cls.recognize_song_keys(id)

        asyncio.run(
            Scanner.reconhecer_artistas_albuns_inexistentes(
                chaves_remover = chaves_para_remover
            )
        )

        CreatePlaylist.remove_path(caminho)
        cls.remove_playlist_json(id = id)
        
    @classmethod
    def recognize_song_keys(cls, id: str):
        json_musicas = Utils.sync_load_json(
            f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Music/musicas.json'
        )
        
        return {
            chave for chave, valor in json_musicas.items()
            if valor.get('id_playlist') == id
        }
    
    @classmethod
    def remove_dead_content(cls, id: str, path: Path):
        from core.meta.scanner.scanner import Scanner

        chaves_para_remover = set()

        json_musicas = Utils.sync_load_json(
            f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Music/musicas.json'
        )

        for chave, valor in json_musicas.items():
            if (
                valor.get('id_playlist') == id and
                valor.get('caminho') != path
            ):
                chaves_para_remover.add(chave)

        asyncio.run(
            Scanner.reconhecer_artistas_albuns_inexistentes(
                chaves_remover = chaves_para_remover
            )
        )

    @classmethod
    def check_playlist_names(cls) -> list[str]:
        nomes_playlists_existentes: set[str] = set()
        
        playlists_json = Utils.sync_load_json(
            AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "playlists.json"
        )
        
        for key, value in playlists_json.get("playlists").items():
            nomes_playlists_existentes.add(value.get("name"))

        return list(nomes_playlists_existentes)
    
    @classmethod
    def check_existing_folders(cls) -> list[str]:

        base_path = AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "playlists"
        
        pastas_existentes = list()

        for playlist in os.listdir(
            base_path
        ):
            config_play_json = Utils.sync_load_json(
                AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "playlists" / playlist / "config_play.json"
            )

            caminho_pasta = config_play_json['music'].get('music_path')

            if caminho_pasta not in pastas_existentes:
                pastas_existentes.append(caminho_pasta)

        return pastas_existentes
    
    @classmethod
    def identify_music_artist(cls, id_musica: str) -> str:
        json_musicas = Utils.sync_load_json(
            f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Music/musicas.json'
        )

        for chave, conteudo in json_musicas.items():
            if chave == id_musica:
                return conteudo.get('artista_final', 'Artista Desconhecido')
            
    @classmethod
    def return_cover(cls, music_name: str) -> Path:
        lista_capas = os.listdir(
            f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Capa Musica'
        )

        for capa in lista_capas:
            if capa == music_name + '.jpg':
                return f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Capa Musica/{capa}'
        return r'Assets\Global\Images\Padrao\capa_musicas_desconhecidas.png'