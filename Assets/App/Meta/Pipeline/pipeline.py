from ..Repository.normalizacao import Filtragem
from Assets.App.Meta.Repository.extrai_metadados import ExtracaoMetadados
from Assets.App.Meta.Controller.status import Status
from ..Models.musica_meta import MusicaMetadados
from .pipeline_fase_1 import PipelineFase1
from .pipeline_fase_2 import PipelineFase2
from .pipeline_fase_3 import PipelineFase3
from ..Repository.tarefas import GerenciaMetadados
from ..Repository.persistencia import Persistencia
from ...Playlists.Controller.estado_playlist import EstadoPlay
import os, asyncio

class Pipeline:
    @classmethod
    async def _async_classificar_presenca(cls, titulo_filtrado : dict[str | None], artista_filtrado : str | None):
        if titulo_filtrado is None:
            return Status.INCOMPLETO

        if titulo_filtrado['artista'] is not None and artista_filtrado is None:
            return Status.SEM_ART_NATIVO

        if titulo_filtrado['artista'] is None and artista_filtrado is not None:
            return Status.SEM_ART_FILTRADO

        if titulo_filtrado['titulo_filtrado'] is not None:
            return Status.APENAS_TITULO

        return Status.INCOMPLETO

    @classmethod
    def normalizar_musica(cls, musica):
        if isinstance(musica, MusicaMetadados):
            return musica.arquivo_mp3_original
        return musica
    
    @classmethod
    def _processar_wrapper_sync(cls, caminho : str, lista_objetos : list = [], id_playlist : str | None = None) -> list[MusicaMetadados]:
        from ..Models.scanner_model import ScannerModel
        from ..Controller.scanner_controller import ScannerController
        from ..Scanner.scanner import Scanner
        from ..Controller.status import StatusScanner
        
        ScannerModel.iniciar_tarefa()
        ScannerModel.definir_status_processo(
            StatusScanner.ON_PIPELINE_PLAYLIST
        )
        Scanner.gerenciar_status()
        ScannerController.notificar(
            'icone_status_scanner',
            None
        )

        try:
            asyncio.run(
                cls._async_processar_musica(
                    caminho = caminho, 
                    lista_objetos = lista_objetos,
                    id = id_playlist
                )
            )
        except Exception as e:
            import traceback

            print(f"[PIPELINE ERROR]: {e}")
            traceback.print_exc()
    
            # notificação de erro
        finally:
            ScannerModel.finalizar_tarefa()
            
            if not ScannerModel.esta_ocupado():
                ScannerModel.definir_status_processo(
                    None
                )
                ScannerController.notificar(
                    'progress_status_scanner',
                    None
                )
                Scanner.gerenciar_status()
                
    @classmethod
    async def _async_processar_musica(cls, caminho : str, lista_objetos : list = [], id : str | None = None) -> list[MusicaMetadados]:
        from ...Services.Controllers.estado_grid import GridMode, EstadoGrid

        lista_já_processadas = []
        lista = []

        for musica in os.listdir(caminho) if len(lista_objetos) == 0 else lista_objetos:
            titulo_filtrado = None
            artista_filtrado = None

            musica = cls.normalizar_musica(musica)
            musica = os.path.basename(musica)

            caminho_arquivo = os.path.normpath(
                os.path.join(caminho, musica)
            )

            # FASE 0 - verificação da existencia de dados já alterados pelo próprio player, assim carregamento dos dados já imbutidos.
            if ExtracaoMetadados.musica_ja_processada(caminho_arquivo):
                mus = ExtracaoMetadados.extrair_metadados_player(caminho_arquivo)

                dic = await asyncio.to_thread(
                    ExtracaoMetadados.extrair_imagens_mp3,
                    caminho_arquivo, 
                    mus, 
                    musica.replace('.mp3', '')
                )

                lista_já_processadas.append(
                    MusicaMetadados(
                        id_playlist = id,
                        titulo_musica_filtrado = mus.get('titulo'),
                        artista_final = mus.get('artista'),
                        arquivo_mp3_original = musica,
                        caminho_musica = caminho,
                        arquivo_mp3_filtrado = None,
                        artista_arquivo_filtrado = None,
                        artista_meta_nativo = mus.get('artista'),
                        artista_titulo_filtrado = None,
                        consenso = None,
                        gap = None,
                        score = None,
                        sim_1 = None,
                        sim_2 = None,
                        lista_artistas_possiveis = [],
                        status = Status.ALTA,
                        titulo_musica_original = musica,
                        img_album = {
                            'id' : mus.get('id_album'), 
                            'nome' : mus.get('album'), 
                            'medium' : dic.get('alb'), 
                            'big' : {
                                'link' : mus.get('imagem_album_player_big'),
                                'caminho' : caminho_arquivo
                            }
                        },
                        img_artista = {
                            'id' : mus.get('id_artista'), 
                            'medium' : dic.get('art'), 
                            'big' : {
                                'link' : mus.get('imagem_album_player_medium'),
                                'caminho' : caminho_arquivo
                            }
                        }
                    )
                )
            else:
                # FASE 1 - extração de metadados e classificação + filtragem tradicional
                dados = await ExtracaoMetadados._async_extrair(caminho_arquivo)
                
                if dados is not None:
                    if dados['titulo'] is not None:
                        titulo_filtrado = await Filtragem._async_filtrar_titulo(nome = dados['titulo'])

                    if dados['artista'] is not None:
                        artista_filtrado = await Filtragem._async_filtrar_artista(artista = dados['artista'])
                
                    if artista_filtrado is not None and titulo_filtrado['artista'] is not None:
                        lista.append(await PipelineFase1._async_fase_1(
                            nome_arquivo_original = musica,
                            titulo_filtrado = titulo_filtrado,
                            artista_meta_nativo = artista_filtrado
                        ))
                    else:
                        lista.append(await ExtracaoMetadados._async_organiza_dados(
                            nome_arquivo_original = musica,
                            titulo_filtrado = titulo_filtrado,
                            artista_meta_nativo = artista_filtrado,
                            status = await cls._async_classificar_presenca(
                                titulo_filtrado = titulo_filtrado, 
                                artista_filtrado = artista_filtrado    
                            ),
                            id_playlist = id
                        ))

        grupos = await PipelineFase2._async_fase_2(
            lista = lista, 
            caminho = caminho
        )
        await PipelineFase3._async_fase_3(
            lista_incompletas = grupos[Status.INCOMPLETO], 
            caminho = caminho
        )
        
        grupos[Status.METADADOS_FASE_0] = lista_já_processadas
        await Persistencia.gerenciar_dados_json_musicas(grupos = grupos)
        await Persistencia.atribuir_memoria()

        EstadoGrid._notificar(
            evento = 'att_grid', 
            dados = GridMode.ARTISTA
        )
        EstadoGrid._notificar(
            evento = 'att_grid',
            dados = GridMode.ALBUM
        )
        
        EstadoPlay.notificar(
            evento = 'att_qtde_play',
            dados = {
                'id' : id,
                'qtde' : len(
                    os.listdir(caminho)
                )
            }
        )