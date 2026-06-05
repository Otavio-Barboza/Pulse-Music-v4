from ...Services.gerenciador_contas import GerenciadorContas
from ...Services.Controllers.estado_grid import EstadoGrid
from ..Repository.persistencia import Persistencia
from ..Controller.status import StatusScanner
from ...Playlists.Controller.estado_playlist import EstadoPlay
from ...Audio.Controller.sessao import SessaoReproducao
import os, asyncio

class Scanner:
    _scanner_rodando = False

    @classmethod
    async def validar_dados_json(cls, dados : dict):
        from ..Models.scanner_model import ScannerModel
        from ...Playlists.Controller.estado_playlist import EstadoPlay, PlaylistCarregada
        from ...Audio.Repository.musica_repositorio import RepositorioMusica

        pasta = dados.get('musicas').get('pasta')
        len_pasta = len(
            os.listdir(pasta)
        )

        dados['musicas']['quantidade_de_musicas'] = len_pasta
       
        musicas_novas = await cls.reconhecer_musicas(
            pasta = pasta, validador = True
        )
        musicas_removidas = await cls.reconhecer_musicas(
            pasta = pasta, validador = False
        )
       
        if musicas_removidas is not None:
            chaves = await cls.obter_chaves_por_caminho(musicas_removidas)
            
            if ScannerModel.esta_ocupado():
                return
            
            await cls.exclusao_musica(
                chaves = chaves
            )
            await Persistencia.atribuir_memoria()
            
            await asyncio.sleep(1)

            if (
                isinstance(EstadoPlay._playlist_aberta, dict) and
                EstadoPlay._playlist_aberta['aberta'] == PlaylistCarregada.ABERTA
            ):
                EstadoPlay.notificar(
                    evento = 'att_musicas_exibidas',
                    dados = pasta
                )

            # if (
            #     len_pasta is not None
            #      or
            #     dados.get('id') is not None
            # ):
            #     EstadoPlay.notificar(
            #         evento = 'att_qtde_play',
            #         dados = {
            #             "id": dados.get('id'), 
            #             "qtde": len_pasta
            #         }
            #     )
        
        if musicas_novas is not None:   
            if ScannerModel.esta_ocupado():
                return
            
            await cls.nova_musica(
                pasta = pasta,
                lista = musicas_novas
            )
            await Persistencia.salvar_json(
                caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists/{dados.get("id")}/config_play.json',
                dados = dados
            )
            await Persistencia.atribuir_memoria()
            
            await asyncio.sleep(1)

            if (
                isinstance(EstadoPlay._playlist_aberta, dict) and
                EstadoPlay._playlist_aberta['aberta'] == PlaylistCarregada.ABERTA
            ):
                EstadoPlay.notificar(
                    evento = 'att_musicas_exibidas',
                    dados = pasta
                )
            
        if (
            len_pasta is not None
            or
            dados.get('id') is not None
        ):
            EstadoPlay.notificar(
                evento = 'att_qtde_play',
                dados = {
                    "id": dados.get('id'), 
                    "qtde": len_pasta
                }
            )            

        await asyncio.sleep(1)

    @classmethod
    async def _async_verificar_json(cls):
        from ..Controller.scanner_controller import ScannerController
        from ..Models.scanner_model import ScannerModel
        
        if cls._scanner_rodando:
            return
        
        cls._scanner_rodando = True
        
        try:
            playlists_disponiveis = os.listdir(
                f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists'
            )
                
            for playlist in playlists_disponiveis:
                dados_playlist = await Persistencia.ler_json(
                    f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'
                )
                await cls.validar_dados_json(dados = dados_playlist)
        finally:
            cls._scanner_rodando = False

    @classmethod
    async def reconhecer_musicas(cls, pasta : str, validador : bool) -> list | None:
        caminhos_json = set()

        musicas_json = await Persistencia.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json'
        )
       
        for _, valor in musicas_json.items():
            if valor.get('caminho') == pasta:
                caminho = os.path.join(
                    valor.get('caminho'),
                    valor.get('arquivo_original')
                )
                caminhos_json.add(
                    os.path.normpath(caminho)
                )
       
        arquivos_pasta = set()

        for arquivo in os.listdir(pasta):
            caminho = os.path.join(
                pasta, 
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
        musica_json = await Persistencia.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json'
        )

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
        from collections import defaultdict
        from ...Meta.Repository.normalizacao import Filtragem
        from ...Services.Controllers.estado_grid import GridMode

        """
            1 - Acessar o JSON musicas.
            2 - Pegar as Imagens das músicas em referência e atribuir em list() ou set().
            3 - Analisar o JSON musicas inteiro e analisar se em alguma música existe aquele artista ou álbum.
                3.1 - SE EXISTIR: Não excluir a imagem do artista/álbum;
                3.2 - SENÃO: Excluir a imagem.
            4 - Excluir a música em si do músicas.json            
        """
        
        musicas_json = await Persistencia.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json'
        )
       
        artistas = defaultdict(set)        
        albuns = defaultdict(set)
        chaves_para_remover = set()
        
        # pegar as imagens
        for chave, valor in musicas_json.items():
            # artista
            artista = Filtragem._limpar_feat(
                valor.get("artista_final")
            )
            artistas[artista].add(chave)           
           
            # albuns
            album = valor.get('album').get('nome_album')            
            albuns[album].add(chave)
                            
        for chave, valor in musicas_json.items():
            artista = Filtragem._limpar_feat(
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
                    f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Capa Musica/{nome_capa_base}.jpg'
                )
                
                if len(restantes_alb) == 0:
                    Persistencia.excluir_imagem(caminho_alb)
                
                if len(restantes_art) == 0:
                    Persistencia.excluir_imagem(caminho_art)
                    
                if os.path.isfile(caminho_capa):
                    Persistencia.excluir_imagem(
                        caminho_capa
                    )
                    
                chaves_para_remover.add(chave)
            
        for chave in chaves_para_remover:
            del musicas_json[chave]
        
        await Persistencia.salvar_json(
            caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json',
            dados = musicas_json
        )            

        EstadoGrid._notificar(
            evento = 'att_grid', 
            dados = GridMode.ARTISTA
        )
        EstadoGrid._notificar(
            evento = 'att_grid',
            dados = GridMode.ALBUM
        )
        
    @classmethod
    async def nova_musica(cls, pasta : str, lista : list):
        from ..Pipeline.pipeline import Pipeline

        caminho_base_playlists = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists'

        for playlist in os.listdir(
            caminho_base_playlists
        ):
            json_config_play = await Persistencia.ler_json(
                f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'
            )

            if json_config_play['musicas'].get('pasta') == pasta:
                playlist_id = playlist
                break
        
        asyncio.create_task(
            asyncio.to_thread(
                Pipeline._processar_wrapper_sync,
                pasta,
                lista,
                playlist_id
            )
        )

    @classmethod
    async def exclusao_musica(cls, chaves : set[str]):       
        from ..Models.scanner_model import ScannerModel
        from ..Controller.scanner_controller import ScannerController
        
        ScannerModel.iniciar_tarefa()
        ScannerModel.definir_status_processo(
            StatusScanner.ON_SCANNER
        )
        cls.gerenciar_status()
        ScannerController.notificar(
            evento = 'icone_status_scanner',
            dados = None
        )
        
        await asyncio.sleep(1)

        try:
            await cls.reconhecer_artistas_albuns_inexistentes(
                chaves_remover = chaves
            )
        finally:
            ScannerModel.finalizar_tarefa()

            await asyncio.sleep(1)

            if not ScannerModel.esta_ocupado():
                ScannerModel.definir_status_processo(
                    None
                )
                ScannerController.notificar(
                    evento = 'progress_status_scanner',
                    dados = None
                )
                cls.gerenciar_status()

    @classmethod
    def gerenciar_status(cls):
        from ..Models.scanner_model import ScannerModel
        from ..Controller.scanner_controller import ScannerController

        if ScannerModel._status_processos == StatusScanner.ON_SCANNER:
            ScannerController.notificar(
                evento = 'informacao_processo_scanner',
                dados = 'Monitoramento está rodando...\n\n    Poder estar havendo remoção dos conteúdos desnecessários ou alguma atualização das informações exibidas.'
            )
        elif ScannerModel._status_processos == StatusScanner.ON_PIPELINE_PLAYLIST:
            ScannerController.notificar(
                evento = 'informacao_processo_scanner',
                dados = 'Buscando dados...\n\n    O player está buscando os dados de artistas, álbuns, capas e todos com suas imagens, aguarde o processo acontecer para visualizá-los.'
            )
        elif ScannerModel._status_processos == None:
            ScannerController.notificar(
                evento = 'informacao_processo_scanner',
                dados = 'Monitor das Playlists aguardando alterações...\n\n    Aqui será indicado as alterações de informações que estiverem acontecendo, sejam:\n\n• Adição de músicas em alguma playlist.\n• Remoção de músicas em alguma playlist.\n\n    O monitor gerencia automaticamente o conteúdo, adicionando novos itens e removendo os desnecessários.'
            )