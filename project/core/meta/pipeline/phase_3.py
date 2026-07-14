from ..Repository.normalizacao import Filtragem
from ..Repository.validacao import Validacao
from Assets.App.Meta.Controller.status import Status
from Assets.App.Meta.Providers.deezer import GerenciadorFontes
from ..Models.musica_meta import MusicaMetadados
from ..Repository.persistencia import Persistencia
from ...Services.gerenciador_contas import GerenciadorContas
from ..Memoria.memoria_artistas import MemoriaArtistas
import aiohttp, os

class PipelineFase3:
    @classmethod
    def _calcular_score_fase3_com_artista(cls, filtro: dict, item: dict):
        return (
            0.6 * Validacao.similaridade(
                filtro["titulo_filtrado"],
                item["title"]
            ) + 0.4 * Validacao.similaridade(
                Filtragem._limpar_feat(filtro["artista"]),
                item["artist"]["name"]
            )
        )
    
    @classmethod
    def _calcular_score_apenas_titulo_fase_3(cls, filtro: dict, item: dict):
        similaridade_titulo = Validacao.similaridade(
            filtro["titulo_filtrado"].lower().strip(),
            item["title"].lower().strip()
        )
        popularidade = item.get("rank", 0) / 1_000_000

        return (0.75 * similaridade_titulo + 0.15 * popularidade)
    
    @classmethod
    async def _resolver_musica_fase_3(cls, fontes : GerenciadorFontes, filtro: dict):
        resultado = await fontes.deezer.buscar_musica(
            titulo = filtro["titulo_filtrado"],
            artista = filtro["artista"]
        )

        if not resultado or not resultado.get("track"):
            return None, 0, None

        itens = resultado["track"]

        # 🔹 CASO 1: TEM ARTISTA NO FILENAME
        if filtro["artista"]:
            melhor_item = None
            melhor_score = 0

            for item in itens:
                score = cls._calcular_score_fase3_com_artista(filtro, item)

                if score > melhor_score:
                    melhor_score = score
                    melhor_item = item

            return melhor_item, melhor_score, None

        # 🔹 CASO 2: APENAS TÍTULO
        else:
            from .phase_2 import PipelineFase2
            
            itens_processados = []

            for item in itens:
                score = cls._calcular_score_apenas_titulo_fase_3(filtro, item)
                item["score_calculado"] = score
                itens_processados.append(item)

            itens_ordenados = sorted(
                itens_processados,
                key = lambda x: x["score_calculado"],
                reverse = True
            )

            top5 = itens_ordenados[:5]

            sim_1 = top5[0]["score_calculado"]
            sim_2 = top5[1]["score_calculado"] if len(top5) > 1 else 0
            gap = sim_1 - sim_2
            consenso, artista_dominante = PipelineFase2._analisar_consenso(top5)

            artista_final, status = await PipelineFase2._classificar_artistas_apenas_titulo(
                gap=gap,
                sim_1=sim_1,
                consenso=consenso,
                top5=top5
            )

            return top5[0], sim_1, {
                "status": status,
                "gap": gap,
                "sim_1": sim_1,
                "sim_2": sim_2,
                "consenso": consenso,
                "artista_final": artista_final
            }
    
    @classmethod
    async def _async_fase_3(cls, lista_incompletas: list[MusicaMetadados], caminho : str):
        from ..Repository.extrai_metadados import ExtracaoMetadados
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fontes = GerenciadorFontes(session)

            for musica in lista_incompletas:

                filtro = await Filtragem._async_filtrar_titulo(
                    musica.arquivo_mp3_original
                )

                musica.set_arquivo_filtrado(filtro['titulo_filtrado'])
                musica.set_artista_arquivo_filtrado(filtro['artista'])
                musica.set_caminho(caminho)
                
                if filtro is None:
                    musica.set_status(Status.BAIXA)
                    musica.set_score(0)
                    musica.set_artista_final(
                        Filtragem._limpar_feat(
                            melhor_item['artist']['name']
                        ) if melhor_item else Filtragem._limpar_feat(
                            filtro['artista']
                        ) or None
                    )  
                    musica.set_artista_id(
                        MemoriaArtistas.resolver_id(
                            musica.artista_final
                        ) if musica.artista_final is not None else None
                    )
                    continue

                melhor_item, melhor_score, dados_apenas_titulo = await cls._resolver_musica_fase_3(fontes, filtro)

                if melhor_item is None:
                    musica.set_status(Status.BAIXA)
                    musica.set_score(0)
                    musica.set_artista_final(
                        Filtragem._limpar_feat(
                            melhor_item['artist']['name']
                        ) if melhor_item else Filtragem._limpar_feat(
                            filtro['artista']
                        ) or None
                    )  
                    musica.set_artista_id(
                        MemoriaArtistas.resolver_id(
                            musica.artista_final
                        ) if musica.artista_final is not None else None
                    )
                    continue

                # 🔹 CASO APENAS TÍTULO
                if dados_apenas_titulo:
                    musica.set_artista_final(
                        Filtragem._limpar_feat(
                            melhor_item['artist']['name']
                        ) if melhor_item else Filtragem._limpar_feat(
                            filtro['artista']
                        ) or None
                    )  
                    musica.set_artista_id(
                        MemoriaArtistas.resolver_id(
                            musica.artista_final
                        ) if musica.artista_final is not None else None
                    )
                    musica.set_status(dados_apenas_titulo["status"])
                    musica.set_score(dados_apenas_titulo["sim_1"])
                    musica.set_gap(dados_apenas_titulo["gap"])
                    musica.set_sim_1(dados_apenas_titulo["sim_1"])
                    musica.set_sim_2(dados_apenas_titulo["sim_2"])
                    musica.set_consenso(dados_apenas_titulo["consenso"])
                    
                    caminho_img_medium_art = Persistencia.baixar_imagem(
                        url = melhor_item['artist']['picture_medium'],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                musica.id_artista + '.jpg'
                            )
                        )
                    )
                    musica.set_imagem_artista(
                        id = melhor_item['artist']['id'] or None,
                        img_m = caminho_img_medium_art,
                        img_b = os.path.normpath(
                            os.path.join(
                                musica.caminho, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['artist']['picture_big'] or None
                    )
                    
                    caminho_img_medium_alb = Persistencia.baixar_imagem(
                        url = melhor_item['album']['cover_medium'],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                melhor_item['album']['title'] + '.jpg'
                            )
                        )
                    )
                    musica.set_imagem_album(
                        nome = melhor_item['album']['title'] or None,
                        id = melhor_item['album']['id'] or None,
                        img_m = caminho_img_medium_alb or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                musica.caminho, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['album']['cover_big'] or None
                    )

                    ExtracaoMetadados.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.caminho, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        titulo = musica.titulo_musica_filtrado if musica.titulo_musica_filtrado is not None else musica.arquivo_mp3_filtrado,
                        artista = musica.artista_final,
                        album = musica.img_album.get('nome'),
                        url_img_album_medium = melhor_item['album']['cover_medium'],
                        url_img_album_big = musica.img_album.get('big').get('link'),
                        url_img_artista_medium = melhor_item['artist']['picture_medium'],
                        url_img_artista_big = musica.img_artista.get('big').get('link'),
                        id_alb = musica.img_artista.get('id'),
                        id_art = musica.img_album.get('id')
                    )
                # 🔹 CASO COM ARTISTA
                else:
                    from .phase_2 import PipelineFase2

                    artista_final = await PipelineFase2._escolher_artista(
                        score = melhor_score,
                        melhor_item = melhor_item,
                        musica = musica
                    )

                    musica.set_artista_final(
                        Filtragem._limpar_feat(
                            melhor_item['artist']['name']
                        ) if melhor_item else Filtragem._limpar_feat(
                            filtro['artista']
                        ) or None
                    )  
                    musica.set_artista_id(
                        MemoriaArtistas.resolver_id(
                            musica.artista_final
                        ) if musica.artista_final is not None else None
                    )

                    musica.set_score(melhor_score)

                    if melhor_score >= 0.85:
                        musica.set_status(Status.ALTA)
                    elif 0.85 > melhor_score > 0.65:
                        musica.set_status(Status.MEDIA)
                    else:
                        musica.set_status(Status.BAIXA)       

                    caminho_img_medium_art = Persistencia.baixar_imagem(
                        url = melhor_item['artist']['picture_medium'],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                musica.id_artista + '.jpg'
                            )
                        )
                    )
                    musica.set_imagem_artista(
                        id = melhor_item['artist']['id'] or None,
                        img_m = caminho_img_medium_art,
                        img_b = os.path.normpath(
                            os.path.join(
                                musica.caminho, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['artist']['picture_big'] or None
                    )
                    
                    caminho_img_medium_alb = Persistencia.baixar_imagem(
                        url = melhor_item['album']['cover_medium'],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                melhor_item['album']['title'] + '.jpg'
                            )
                        )
                    )
                    musica.set_imagem_album(
                        nome = melhor_item['album']['title'] or None,
                        id = melhor_item['album']['id'] or None,
                        img_m = caminho_img_medium_alb or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                musica.caminho, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['album']['cover_big'] or None
                    )

                    ExtracaoMetadados.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.caminho, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        titulo = musica.titulo_musica_filtrado if musica.titulo_musica_filtrado is not None else musica.arquivo_mp3_filtrado,
                        artista = musica.artista_final,
                        album = musica.img_album.get('nome'),
                        url_img_album_medium = melhor_item['album']['cover_medium'],
                        url_img_album_big = musica.img_album.get('big').get('link'),
                        url_img_artista_medium = melhor_item['artist']['picture_medium'],
                        url_img_artista_big = musica.img_artista.get('big').get('link'),
                        id_alb = musica.img_artista.get('id'),
                        id_art = musica.img_album.get('id')
                    )

        await Pipeline.salvar_dados(
            {Status.INCOMPLETO : lista_incompletas}
        )
        Pipeline.executar_callbacks(caminho)