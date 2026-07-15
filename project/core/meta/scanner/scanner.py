# imports de back-end
from core.services.account_manager import AccountManager
from core.services.controllers.grid_state import GridState
from core.meta.repository.metadata_repository import MetadataRepository
from core.meta.enum.status import ScannerStatus
from core.playlists.controller.playlist_state import PlaylistState
from core.playlists.enum.playlist_enum import PlaylistLoaded
from core.meta.controller.scanner_controller import ScannerController
from core.services.controllers.grid_state import GridMode
from core.meta.repository.filtering import Filtering

# imports gerais
from collections import defaultdict
import os, asyncio


class Scanner:

    _is_running = False

    @classmethod
    async def validar_dados_json(cls, data : dict):
        from core.meta.models.scanner_model import ScannerModel

        path = data.get('songs').get('path')
        len_path = len(os.listdir(path))

        data['songs']['quantidade_de_musicas'] = len_path
       
        new_songs = await cls.identify_songs(
            path = path, validate = True
        )
        removed_songs = await cls.identify_songs(
            path = path, validate = False
        )
       
        if removed_songs is not None:
            keys = await cls.get_key_for_path(removed_songs)
            
            if ScannerModel.return_is_busy():
                return
            
            await cls.delete_music(
                keys = keys
            )
            await MetadataRepository.load_cache()
            
            await asyncio.sleep(1)

            if (
                isinstance(PlaylistState.playlist_loaded, dict) and
                PlaylistState.playlist_loaded['open'] == PlaylistLoaded.ABERTA
            ):
                PlaylistState.notify(
                    event = 'update_displayed_musics',
                    data = path
                )

        if new_songs is not None:   
            if ScannerModel.esta_ocupado():
                return
            
            await cls.new_song(
                path = path,
                list = new_songs
            )
            await MetadataRepository.save_artists_json(
                # path = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists/{data.get("id")}/config_play.json',
                data = data
            )
            await MetadataRepository.load_cache()
            
            await asyncio.sleep(1)

            if (
                isinstance(PlaylistState.playlist_loaded, dict) and
                PlaylistState.playlist_loaded['open'] == PlaylistLoaded.OPEN 
            ):
                PlaylistState.notify(
                    event = 'update_displayed_musics',
                    data = path
                )
            
        if (
            len_path is not None
            or data.get('id') is not None
        ):
            PlaylistState.notify(
                event = 'att_qtde_play',
                data = {
                    "id": data.get('id'), 
                    "qtde": len_path
                }
            )            

        await asyncio.sleep(1)

    @classmethod
    async def _verify_json(cls):
        if cls._is_running:
            return
        
        cls._is_running = True
        
        try:
            available_playlists = os.listdir(
                f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists'
            )
                
            for playlist in available_playlists:
                data_playlist = await MetadataRepository.return_artists_json()
                    # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'

                await cls.validar_dados_json(data = data_playlist)
        finally:
            cls._is_running = False

    @classmethod
    async def identify_songs(cls, path: str, validate: bool) -> list | None:
        paths_json = set()

        song_json = await MetadataRepository.return_artists_json()
            # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/songs.json'
       
        for _, value in song_json.items():
            if value.get('path') == path:
                path = os.path.join(
                    value.get('song_path'),
                    value.get('mp3_file')
                )
                paths_json.add(
                    os.path.normpath(path)
                )
       
        path_files = set()

        for file in os.listdir(path):
            path = os.path.join(
                path, 
                file
            )

            if os.path.isfile(path) and file.lower().endswith('.mp3'):
                path_files.add(
                    os.path.normpath(path)
                )
       
        list_to_return = list(path_files - paths_json) if validate else list(paths_json - path_files)
           
        return list_to_return if len(list_to_return) != 0 else None
    
    @classmethod
    async def get_key_for_path(cls, paths : list[str]) -> set[str]:
        songs_json = await MetadataRepository.return_artists_json()
            # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/songs.json'

        paths = set(os.path.normpath(c) for c in paths)

        return {
            key for key, value in songs_json.items()
            if os.path.normpath(
                os.path.join(
                    value.get('path'), 
                    value.get('arquivo_original')
                )
            ) in paths
        }
    
    @classmethod
    async def identify_artists_albums_existings(cls, keys_to_remove: set[str]):
        """
            1 - Acessar o JSON songs.
            2 - Pegar as Imagens das músicas em referência e atribuir em list() ou set().
            3 - Analisar o JSON songs inteiro e analisar se em alguma música existe aquele artist ou álbum.
                3.1 - SE EXISTIR: Não excluir a imagem do artist/álbum;
                3.2 - SENÃO: Excluir a imagem.
            4 - Excluir a música em si do músicas.json            
        """
        
        song_json = await MetadataRepository.return_artists_json()
            # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/songs.json'
       
        artists = defaultdict(set)        
        albums = defaultdict(set)
        keys_for_remove = set()
        
        # pegar as imagens
        for key, value in song_json.items():
            # artist
            artist = Filtering.clean_feat(
                value.get("artista_final")
            )
            artists[artist].add(key)           
           
            # albums
            album = value.get('album').get('name')            
            albums[album].add(key)
                            
        for key, value in song_json.items():
            artist = Filtering.clean_feat(
                value.get("defined_artist")
            )
            album = value.get('album').get('name')

            caminho_art = value.get('artist').get('img_medium')
            caminho_alb = value.get('album').get('img_medium')
            
            # album
            if key in keys_to_remove:
                remaining_alb = albums[album] - keys_to_remove
                remaining_art = artists[artist] - keys_to_remove

                cover_name, _ = os.path.splitext(
                    value.get('arquivo_original')
                )
                cover_path = os.path.normpath(
                    f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Capa Musica/{cover_name}.jpg'
                )
                
                if len(remaining_alb) == 0:
                    MetadataRepository.delete_image(caminho_alb)
                
                if len(remaining_art) == 0:
                    MetadataRepository.delete_image(caminho_art)
                    
                if os.path.isfile(cover_path):
                    MetadataRepository.delete_image(cover_path)
                    
                keys_for_remove.add(key)
            
        lyrics_json = await MetadataRepository.return_artists_json()
            # path = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/letras.json'

        for key in keys_for_remove:
            del song_json[key]
            del lyrics_json[key]
        
        await MetadataRepository.save_artists_json(
            # path = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/songs.json',
            data = song_json
        )            
        await MetadataRepository.save_artists_json(
            path = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/letras.json',
            data = lyrics_json
        )            

        GridState.notify(
            event = 'att_grid', 
            data = GridMode.ARTIST
        )
        GridState.notify(
            event = 'att_grid',
            data = GridMode.ALBUM
        )
        
    @classmethod
    async def new_song(cls, path: str, list: list):
        from core.meta.pipeline.pipeline import Pipeline

        base_path_playlists = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists'

        for playlist in os.listdir(
            base_path_playlists
        ):
            json_config_play = await MetadataRepository.return_artists_json(
                f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'
            )

            if json_config_play['songs'].get('path') == path:
                playlist_id = playlist
                break
        
        asyncio.create_task(
            asyncio.to_thread(
                Pipeline.processar_wrapper_sync,
                path,
                list,
                playlist_id
            )
        )

    @classmethod
    async def delete_music(cls, keys : set[str]):       
        from core.meta.models.scanner_model import ScannerModel

        ScannerModel.start_task()
        ScannerModel.set_status_prosesses(ScannerStatus.ON_SCANNER)
        cls.manager_status()

        ScannerController.notify(
            event = 'icon_status_scanner',
            data = None
        )
        
        await asyncio.sleep(1)

        try:
            await cls.identify_artists_albums_existings(
                keys_to_remove = keys
            )
        finally:
            ScannerModel.finalizar_tarefa()

            await asyncio.sleep(1)

            if not ScannerModel.esta_ocupado():
                ScannerModel.definir_status_processo(
                    None
                )
                ScannerController.notify(
                    event = 'progress_status_scanner',
                    data = None
                )
                cls.manager_status()

    @classmethod
    def manager_status(cls):
        from core.meta.models.scanner_model import ScannerModel

        if ScannerModel.status_procesesses == ScannerStatus.ON_SCANNER:
            ScannerController.notify(
                event = 'processes_information_scanner',
                data = 'Monitoramento está rodando...\n\n    Poder estar havendo remoção dos conteúdos desnecessários ou alguma atualização das informações exibidas.'
            )
        elif ScannerModel.status_procesesses == ScannerStatus.ON_PIPELINE_PLAYLIST:
            ScannerController.notify(
                event = 'processes_information_scanner',
                data = 'Buscando data...\n\n    O player está buscando os data de artists, álbuns, capas e todos com suas imagens, aguarde o processo acontecer para visualizá-los.'
            )
        elif ScannerModel.status_procesesses == None:
            ScannerController.notify(
                event = 'processes_information_scanner',
                data = 'Monitor das Playlists aguardando alterações...\n\n    Aqui será indicado as alterações de informações que estiverem acontecendo, sejam:\n\n• Adição de músicas em alguma playlist.\n• Remoção de músicas em alguma playlist.\n\n    O monitor gerencia automaticamente o conteúdo, adicionando novos itens e removendo os desnecessários.'
            )