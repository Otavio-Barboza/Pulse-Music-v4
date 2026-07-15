# imports de back-end
from project.core.services.account_manager import AccountManager
from project.core.services.controllers.grid_state import GridState
from project.core.meta.repository.metadata_repository import MetadataRepository
from project.core.meta.enum.status import ScannerStatus
from project.core.playlists.controller.playlist_state import PlaylistState
from project.core.playlists.enum.playlist_enum import PlaylistLoaded
from project.core.meta.controller.scanner_controller import ScannerController
from project.core.services.controllers.grid_state import GridMode
from project.core.meta.repository.filtering import Filtering

# imports gerais
from collections import defaultdict
import os, asyncio


class Scanner:

    _is_running = False

    @classmethod
    async def validar_dados_json(cls, data : dict):
        from project.core.meta.models.scanner_model import ScannerModel

        path = data.get('musicas').get('path')
        len_path = len(os.listdir(path))

        data['musicas']['quantidade_de_musicas'] = len_path
       
        new_songs = await cls.reconhecer_musicas(
            path = path, validador = True
        )
        removed_songs = await cls.reconhecer_musicas(
            path = path, validador = False
        )
       
        if removed_songs is not None:
            keys = await cls.obter_chaves_por_caminho(removed_songs)
            
            if ScannerModel.return_is_busy():
                return
            
            await cls.exclusao_musica(
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
            
            await cls.nova_musica(
                path = path,
                list = new_songs
            )
            await MetadataRepository.save_artists_json(
                # caminho = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists/{data.get("id")}/config_play.json',
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
    async def _async_verificar_json(cls):
        if cls._is_running:
            return
        
        cls._is_running = True
        
        try:
            playlists_disponiveis = os.listdir(
                f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists'
            )
                
            for playlist in playlists_disponiveis:
                dados_playlist = await MetadataRepository.return_artists_json()
                    # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'

                await cls.validar_dados_json(data = dados_playlist)
        finally:
            cls._is_running = False

    @classmethod
    async def reconhecer_musicas(cls, path : str, validador : bool) -> list | None:
        caminhos_json = set()

        musicas_json = await MetadataRepository.return_artists_json()
            # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/musicas.json'
       
        for _, valor in musicas_json.items():
            if valor.get('caminho') == path:
                caminho = os.path.join(
                    valor.get('caminho'),
                    valor.get('arquivo_original')
                )
                caminhos_json.add(
                    os.path.normpath(caminho)
                )
       
        arquivos_pasta = set()

        for arquivo in os.listdir(path):
            caminho = os.path.join(
                path, 
                arquivo
            )

            if os.path.isfile(caminho) and arquivo.lower().endswith('.mp3'):
                arquivos_pasta.add(
                    os.path.normpath(caminho)
                )
       
        lista_a_retornar = list(arquivos_pasta - caminhos_json) if validador else list(caminhos_json - arquivos_pasta)
           
        return lista_a_retornar if len(lista_a_retornar) != 0 else None
    
    @classmethod
    async def obter_chaves_por_caminho(cls, caminhos : list[str]) -> set[str]:
        musica_json = await MetadataRepository.return_artists_json()
            # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/musicas.json'

        caminhos = set(os.path.normpath(c) for c in caminhos)

        return {
            chave for chave, valor in musica_json.items()
            if os.path.normpath(
                os.path.join(
                    valor.get('caminho'), 
                    valor.get('arquivo_original')
                )
            ) in caminhos
        }
    
    @classmethod
    async def reconhecer_artistas_albuns_inexistentes(cls, chaves_remover : set[str]):
        """
            1 - Acessar o JSON musicas.
            2 - Pegar as Imagens das músicas em referência e atribuir em list() ou set().
            3 - Analisar o JSON musicas inteiro e analisar se em alguma música existe aquele artista ou álbum.
                3.1 - SE EXISTIR: Não excluir a imagem do artista/álbum;
                3.2 - SENÃO: Excluir a imagem.
            4 - Excluir a música em si do músicas.json            
        """
        
        musicas_json = await MetadataRepository.return_artists_json()
            # f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/musicas.json'
       
        artistas = defaultdict(set)        
        albuns = defaultdict(set)
        chaves_para_remover = set()
        
        # pegar as imagens
        for chave, valor in musicas_json.items():
            # artista
            artista = Filtering.clean_feat(
                valor.get("artista_final")
            )
            artistas[artista].add(chave)           
           
            # albuns
            album = valor.get('album').get('nome_album')            
            albuns[album].add(chave)
                            
        for chave, valor in musicas_json.items():
            artista = Filtering.clean_feat(
                valor.get("artista_final")
            )
            album = valor.get('album').get('nome_album')

            caminho_art = valor.get('artista').get('img_medium')
            caminho_alb = valor.get('album').get('img_medium')
            
            # album
            if chave in chaves_remover:
                restantes_alb = albuns[album] - chaves_remover
                restantes_art = artistas[artista] - chaves_remover

                nome_capa_base, _ = os.path.splitext(
                    valor.get('arquivo_original')
                )
                caminho_capa = os.path.normpath(
                    f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Capa Musica/{nome_capa_base}.jpg'
                )
                
                if len(restantes_alb) == 0:
                    MetadataRepository.delete_image(caminho_alb)
                
                if len(restantes_art) == 0:
                    MetadataRepository.delete_image(caminho_art)
                    
                if os.path.isfile(caminho_capa):
                    MetadataRepository.delete_image(
                        caminho_capa
                    )
                    
                chaves_para_remover.add(chave)
            
        letras_json = await MetadataRepository.return_artists_json()
            # caminho = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/letras.json'

        for chave in chaves_para_remover:
            del musicas_json[chave]
            del letras_json[chave]
        
        await MetadataRepository.save_artists_json(
            # caminho = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/musicas.json',
            data = musicas_json
        )            
        await MetadataRepository.save_artists_json(
            caminho = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/letras.json',
            data = letras_json
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
    async def nova_musica(cls, path : str, list: list):
        from project.core.meta.pipeline.pipeline import Pipeline

        caminho_base_playlists = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists'

        for playlist in os.listdir(
            caminho_base_playlists
        ):
            json_config_play = await MetadataRepository.return_artists_json(
                f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'
            )

            if json_config_play['musicas'].get('path') == path:
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
    async def exclusao_musica(cls, keys : set[str]):       
        from project.core.meta.models.scanner_model import ScannerModel

        ScannerModel.start_task()
        ScannerModel.set_status_prosesses(ScannerStatus.ON_SCANNER)
        cls.gerenciar_status()
        ScannerController.notify(
            event = 'icon_status_scanner',
            data = None
        )
        
        await asyncio.sleep(1)

        try:
            await cls.reconhecer_artistas_albuns_inexistentes(
                chaves_remover = keys
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
                cls.gerenciar_status()

    @classmethod
    def gerenciar_status(cls):
        from project.core.meta.models.scanner_model import ScannerModel

        if ScannerModel.status_procesesses == ScannerStatus.ON_SCANNER:
            ScannerController.notify(
                event = 'processes_information_scanner',
                data = 'Monitoramento está rodando...\n\n    Poder estar havendo remoção dos conteúdos desnecessários ou alguma atualização das informações exibidas.'
            )
        elif ScannerModel.status_procesesses == ScannerStatus.ON_PIPELINE_PLAYLIST:
            ScannerController.notify(
                event = 'processes_information_scanner',
                data = 'Buscando data...\n\n    O player está buscando os data de artistas, álbuns, capas e todos com suas imagens, aguarde o processo acontecer para visualizá-los.'
            )
        elif ScannerModel.status_procesesses == None:
            ScannerController.notify(
                event = 'processes_information_scanner',
                data = 'Monitor das Playlists aguardando alterações...\n\n    Aqui será indicado as alterações de informações que estiverem acontecendo, sejam:\n\n• Adição de músicas em alguma playlist.\n• Remoção de músicas em alguma playlist.\n\n    O monitor gerencia automaticamente o conteúdo, adicionando novos itens e removendo os desnecessários.'
            )