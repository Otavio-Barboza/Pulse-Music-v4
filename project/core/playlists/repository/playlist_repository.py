# imports de back-end
from core.utils.utils import Utils
from core.services.account_manager import AccountManager
from core.playlists.models.playlist import Playlist
from core.playlists.models.playlist_config import PlaylistConfig
from core.playlists.models.playlist_card import PlaylistCard
from core.playlists.repository.path import CreatePlaylist

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
        lista_plays = []
        CAMINHO_JSON_PLAYLIST = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/playlists.json'
        playlists = Utils.sync_load_json(CAMINHO_JSON_PLAYLIST)

        for p in playlists['playlists']:
            if p != 'favoritas':
                id_play = playlists['playlists'].get(p)
                nome_play = id_play.get('nome')
                tipo_play = id_play.get('tipo')

                lista_plays.append(Playlist(
                    id = p,
                    nome = nome_play
                ))
        
        return lista_plays
    
    @classmethod
    def load_cards(cls) -> list[PlaylistCard]:
        """
            Com auxílio do cls.carregar_itens utiliza-se dos objetos Playlist() e com eles carrega os detalhes de cada playlist, armazenando-os na lista cards os objetos PlaylistCard().
        Returns:
            list[PlaylistCard]: Lista com objetos PlaylistCard()
        """
        usuario = AccountManager.accounts_cache
        playlists = cls.carregar_itens()
        cards = []

        for pl in playlists:
            cfg = Utils.sync_load_json(
                cam = f'Assets/Data/Contas/{usuario["current_account"]}/Playlists/{pl.id}/config_play.json'
            )
            
            caminho = cfg['musicas']['pasta']
            qtde = CreatePlaylist.count_number_of_songs(caminho)

            cards.append(PlaylistCard(
                id = pl.id,
                name = cfg['nome'],
                image_path = cfg['style']['pasta'],
                color = cfg['style']['cor'],
                opacity = cfg['style']['opacidade'],
                playlist_path = caminho,
                number_of_songs = qtde
            ))
        
        return cards
    
    @classmethod
    def list_playlists(cls) -> list[PlaylistCard]:
        """
            Chama cls.load_cards para intermediar o retorno das playlists ao EstadoPlaylist
        Returns:
            list[PlaylistCard]: lista com objetos PlaylistCard()
        """
        return cls.load_cards()
    
    @classmethod
    def count_number_of_songs(cls, path: Path) -> int:
        """
            Intermédio para EstadoPlaylist e outras chamadas do contador da quantidade de músicas da playlist.
        Args:
            path (str): caminho da pasta

        Returns:
            int: N° int da quantidade de músicas da playlist
        """
        return CreatePlaylist.count_number_of_songs(path)

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

        usuario = AccountManager.accounts_cache
        CAMINHO_JSON_PLAYLIST = f'Assets/Data/Contas/{usuario["current_account"]}/playlists.json'
        dados = Utils.sync_load_json(CAMINHO_JSON_PLAYLIST)

        novo_id, id_num = CreatePlaylist.generate_id(dados = dados)
        dados['ultimo_id'] = id_num
        
        PASTA_PLAYLIST = f'Assets/Data/Contas/{usuario["current_account"]}/Playlists/{novo_id}'
        JSON_CONFIG_PLAYLIST = f'Assets/Data/Contas/{usuario["current_account"]}/Playlists/{novo_id}/config_play.json'
        JSON_MUSICAS_PLAYLIST = f'Assets/Data/Contas/{usuario["current_account"]}/Music/musicas.json'
        qtde = CreatePlaylist.count_number_of_songs(music_path)

        json_config = CreatePlaylist.return_content_data_playlits(
            id = novo_id,
            music_path = music_path,
            image_path = image_path,
            color = color,
            opacity = opacity,
            name = name,
            number_of_songs = qtde
        )
        dados['playlists'][novo_id] = CreatePlaylist.return_name_playlist_json(name)
        dados['latest_aztualization'] = CreatePlaylist.generate_date()

        Utils.create_path(PASTA_PLAYLIST)
        Utils.sync_update_json(
            path = JSON_CONFIG_PLAYLIST,
            data = json_config
        )

        if not Path(JSON_MUSICAS_PLAYLIST).exists():
            Utils.sync_update_json(
                path = JSON_MUSICAS_PLAYLIST,
                data = {}
            )
         
        return Playlist(
            id = novo_id,
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
        from ...Meta.Scanner.scanner import Scanner
        
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
        from ...Meta.Scanner.scanner import Scanner
        import asyncio

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
        caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Playlists'
        nomes_playlists_existentes = list()

        for c in os.listdir(
            caminho
        ):
            config_play_json = Utils.sync_load_json(
                f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Playlists/{c}/config_play.json'
            )

            nome = config_play_json.get('nome')

            if nome not in nomes_playlists_existentes:
                nomes_playlists_existentes.append(nome)

        return nomes_playlists_existentes
    
    @classmethod
    def check_existing_folders(cls) -> list[str]:
        caminho_base = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Playlists'
        pastas_existentes = list()

        for playlist in os.listdir(
            caminho_base
        ):
            config_play_json = Utils.sync_load_json(
                f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Playlists/{playlist}/config_play.json'
            )

            caminho_pasta = config_play_json['musicas'].get('pasta')

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