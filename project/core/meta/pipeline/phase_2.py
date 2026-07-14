# imports de back-end
from project.core.meta.repository.filtering import Filtering
from project.core.meta.repository.tasks import Task
from project.core.meta.enum.status import SongStatus
from project.core.meta.provider.deezer import FontManager
from project.core.meta.models.song import SongMetadata
from project.core.meta.repository.extract_metadata import ExtractMetadata
from project.core.meta.cache.cache_artists import CacheArtists
from project.core.services.account_manager import AccountManager       

# imports gerais
import aiohttp, os


class Phase2:
    @classmethod
    async def phase_2(cls, list_object: list[SongMetadata], path : str):
        groups = {
            SongStatus.BOTH : [],
            SongStatus.MEDIUM : [],
            SongStatus.INCONSISTENT : [],
            SongStatus.INCOMPLETE : [],
            SongStatus.TITLE_ONLY : [],
            SongStatus.NO_ARTIST_FILTERED : [],
            SongStatus.NO_ARTIST_ID3 : []
        }
        
        if list_object is None:
            raise(f'ERRO: {type(list_object)}')
        
        # organização dos dados
        for data in list_object:
            groups[data.status].append(data)

        await cls.resolve_both(
            lista_ambos = groups[SongStatus.BOTH], 
            path = path
        )
        await cls.resolve_medium_and_inconsistent(
            inconsitent_list = groups[SongStatus.INCONSISTENT],
            medium_list = groups[SongStatus.MEDIUM],
            path = path
        )
        await cls.resolve_no_artist_filtered_or_no_id3(
            filtered_only_list = groups[SongStatus.NO_ARTIST_ID3],
            id3_only_list = groups[SongStatus.NO_ARTIST_FILTERED],
            path = path
        )
        await cls.resolve_title_only(
            title_only_list = groups[SongStatus.TITLE_ONLY],
            path = path
        )

        return groups
    
    @classmethod
    async def resolve_both(cls, lista_ambos : list[SongMetadata], path : str):
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)

            for musica in lista_ambos:
                musica.set_artista_final(
                    Filtering._limpar_feat(musica.artista_titulo_filtrado)
                )
                musica.set_artista_id(
                    CacheArtists.resolver_id(
                        musica.artista_final
                    ) if musica.artista_final is not None else None
                )
                musica.set_possiveis_artistas([musica.artista_meta_nativo])
                musica.set_status(SongStatus.ALTA)
                musica.set_score(1.5)
                musica.set_caminho(path)
                
                dados_deezer = await fonts.deezer.buscar_musica(titulo = musica.titulo_musica_filtrado, artista = musica.artista_final)
                
                caminho_img_medium_art = Persistencia.baixar_imagem(
                    url = dados_deezer['track'][0]['artist']['picture_medium'],
                    caminho_destino = os.path.normpath(
                        os.path.join(
                            CAMINHO_ARTISTAS, 
                            musica.id_artista + '.jpg'
                        )
                    )
                )
                musica.set_imagem_artista(
                    id = dados_deezer['track'][0]['artist']['id'] or None,
                    img_m = caminho_img_medium_art,
                    img_b = os.path.normpath(
                        os.path.join(
                            musica.path, 
                            musica.arquivo_mp3_original
                        )
                    ),
                    img_b_link = dados_deezer['track'][0]['artist']['picture_big'] or None
                )

                caminho_img_medium_alb = Persistencia.baixar_imagem(
                    url = dados_deezer['track'][0]['album']['cover_medium'],
                    caminho_destino = os.path.normpath(
                        os.path.join(
                            CAMINHO_ALBUNS, 
                            dados_deezer['track'][0]['album']['title'] + '.jpg'
                        )
                    )
                )
                musica.set_imagem_album(
                    nome = dados_deezer['track'][0]['album']['title'] or None,
                    id = dados_deezer['track'][0]['album']['id'] or None,
                    img_m = caminho_img_medium_alb or None,
                    img_b = os.path.normpath(
                        os.path.join(
                            musica.path, 
                            musica.arquivo_mp3_original
                        )
                    ),
                    img_b_link = dados_deezer['track'][0]['album']['cover_big'] or None
                )

                ExtractMetadata.registrar_metadados_player(
                    caminho_arquivo = os.path.normpath(
                        os.path.join(
                            musica.path, 
                            musica.arquivo_mp3_original
                        )
                    ),
                    titulo = musica.titulo_musica_filtrado if musica.titulo_musica_filtrado is not None else musica.arquivo_mp3_filtrado,
                    artista = musica.artista_final,
                    album = musica.img_album.get('nome'),
                    url_img_album_medium = dados_deezer['track'][0]['album']['cover_medium'],
                    url_img_album_big = musica.img_album.get('big').get('link'),
                    url_img_artista_medium = dados_deezer['track'][0]['artist']['picture_medium'],
                    url_img_artista_big = musica.img_artista.get('big').get('link'),
                    id_alb = musica.img_artista.get('id'),
                    id_art = musica.img_album.get('id')
                )

        await Pipeline.salvar_dados(
            {SongStatus.AMBOS : lista_ambos}
        )
        Pipeline.executar_callbacks(path)
    
    @classmethod
    async def _resolver_musica(cls, fonts : FontManager, musica : SongMetadata, estrategia : dict):
        artista_para_busca = estrategia['artista_para_busca'](musica)

        resultado = await fonts.deezer.buscar_musica(
            titulo = musica.titulo_musica_filtrado,
            artista = artista_para_busca
        )

        if not resultado.get('track'):
            return None, 0
        
        melhor_item = None
        melhor_score = 0

        for item in resultado['track']:
            score = estrategia['calcular_score'](musica, item)

            if score > melhor_score:
                melhor_score = score
                melhor_item = item
        
        return melhor_item, melhor_score
    
    @classmethod
    async def _escolher_artista(cls, score : float, melhor_item : dict, musica : SongMetadata):
        if score >= 0.85:
            return melhor_item['artist']['name']
        elif 0.85 > score > 0.65:
            return musica.artista_titulo_filtrado or musica.artista_meta_nativo
        else:
            return musica.artista_meta_nativo or musica.artista_titulo_filtrado
        
    @classmethod
    def _estrategia_medios(cls):
        return {
            'artista_para_busca' : lambda musica: Filtering._limpar_feat(musica.artista_titulo_filtrado),
            'calcular_score' : lambda musica, item: (
                0.6 * Task.similaridade(
                    musica.titulo_musica_filtrado,
                    item['title']
                ) + 0.4 * max(
                    Task.similaridade(
                        Filtering._limpar_feat(musica.artista_titulo_filtrado),
                        item['artist']['name']
                    ),
                    Task.similaridade(
                        musica.artista_meta_nativo,
                        item['artist']['name']
                    )
                )
            )
        }
    
    @classmethod
    async def resolve_medium_and_inconsistent(cls, medium_list : list[SongMetadata], inconsitent_list : list[SongMetadata], path : str):
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)

            for musica in medium_list:
                melhor_item, melhor_score = await cls._resolver_musica(
                    musica = musica,
                    fonts = fonts,
                    estrategia = cls._estrategia_medios()
                )
                artista_final = await cls._escolher_artista(
                    score = melhor_score,
                    melhor_item = melhor_item,
                    musica = musica
                )

                musica.set_artista_final(
                    Filtering._limpar_feat(artista_final)
                )
                musica.set_artista_id(
                    CacheArtists.resolver_id(
                        musica.artista_final
                    ) if musica.artista_final is not None else None
                )

                musica.set_score(melhor_score)
                musica.set_possiveis_artistas([melhor_item['artist']['name'] if melhor_item is not None else 'Desconhecido', musica.artista_titulo_filtrado, musica.artista_meta_nativo])  
                musica.set_caminho(path)
                
                if melhor_score >= 0.85:
                    musica.set_status(SongStatus.ALTA)
                elif 0.85 > melhor_score > 0.65:
                    musica.set_status(SongStatus.MEDIA)
                else:
                    musica.set_status(SongStatus.BAIXA)

                if melhor_item is not None:

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
                                musica.path, 
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
                                musica.path, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.path, 
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

            for musica in inconsitent_list:
                melhor_item, melhor_score = await cls._resolver_musica(
                    musica = musica,
                    fonts = fonts,
                    estrategia = cls._estrategia_medios()
                )
                artista_final = await cls._escolher_artista(
                    score = melhor_score,
                    melhor_item = melhor_item,
                    musica = musica
                )

                musica.set_artista_final(
                    Filtering._limpar_feat(artista_final)
                )
                musica.set_artista_id(
                    CacheArtists.resolver_id(
                        musica.artista_final
                    ) if musica.artista_final is not None else None
                )

                musica.set_score(melhor_score)
                musica.set_possiveis_artistas([melhor_item['artist']['name'] if melhor_item is not None else 'Desconhecido', musica.artista_titulo_filtrado, musica.artista_meta_nativo])
                musica.set_caminho(path)

                if melhor_score >= 0.85:
                    musica.set_status(SongStatus.ALTA)
                elif 0.85 > melhor_score > 0.65:
                    musica.set_status(SongStatus.MEDIA)
                else:
                    musica.set_status(SongStatus.BAIXA)

                if melhor_item is not None:

                    caminho_img_medium_art =  Persistencia.baixar_imagem(
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
                                musica.path, 
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
                                musica.path, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.path, 
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
            {
                SongStatus.MEDIO : medium_list,
                SongStatus.INCONSISTENTE : inconsitent_list
            }
        )
        Pipeline.executar_callbacks(path)

    @classmethod
    def _estrategia_artista_filtrado(cls):
        return {
            'artista_para_busca' : lambda musica: Filtering._limpar_feat(musica.artista_titulo_filtrado),
            'calcular_score' : lambda musica, item: (
                0.6 * Task.similaridade(
                    musica.titulo_musica_filtrado,
                    item['title']
                ) + 0.4 * Task.similaridade(
                    musica.artista_titulo_filtrado,
                    item['artist']['name']
                )
            )
        }
    
    @classmethod
    def _estrategia_artista_nativo(cls):
        return {
            'artista_para_busca' : lambda musica: musica.artista_meta_nativo,
            'calcular_score' : lambda musica, item: (
                0.6 * Task.similaridade(
                    musica.titulo_musica_filtrado,
                    item['title']
                ) + 0.4 * Task.similaridade(
                    musica.artista_meta_nativo,
                    item['artist']['name']
                )
            )
        }
    
    @classmethod
    async def resolve_no_artist_filtered_or_no_id3(cls, id3_only_list : list[SongMetadata], filtered_only_list : list[SongMetadata], path : str):
        from .pipeline import Pipeline
        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)
            lista = []

            for musica in filtered_only_list:
                melhor_item, melhor_score = await cls._resolver_musica(
                    fonts = fonts,
                    musica = musica,
                    estrategia = cls._estrategia_artista_filtrado()
                )
                artista_final = await cls._escolher_artista(
                    score = melhor_score,
                    melhor_item = melhor_item,
                    musica = musica
                )

                musica.set_artista_final(
                    Filtering._limpar_feat(artista_final)
                )
                musica.set_artista_id(
                    CacheArtists.resolver_id(
                        musica.artista_final
                    ) if musica.artista_final is not None else None
                )

                musica.set_score(melhor_score)
                musica.set_possiveis_artistas([melhor_item['artist']['name'] if melhor_item is not None else 'Desconhecido', musica.artista_meta_nativo])  
                musica.set_caminho(path)
                
                if melhor_score >= 0.85:
                    musica.set_status(SongStatus.ALTA)
                elif 0.85 > melhor_score > 0.65:
                    musica.set_status(SongStatus.MEDIA)
                else:
                    musica.set_status(SongStatus.BAIXA)

                if melhor_item is not None:

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
                                musica.path, 
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
                                musica.path, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.path, 
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

            for musica in id3_only_list:
                melhor_item, melhor_score = await cls._resolver_musica(
                    fonts = fonts,
                    musica = musica,
                    estrategia = cls._estrategia_artista_nativo()
                )
                artista_final = await cls._escolher_artista(
                    score = melhor_score,
                    melhor_item = melhor_item,
                    musica = musica
                )

                musica.set_artista_final(
                    Filtering._limpar_feat(artista_final)
                )
                musica.set_artista_id(
                    CacheArtists.resolver_id(
                        musica.artista_final
                    ) if musica.artista_final is not None else None
                )

                musica.set_score(melhor_score)
                musica.set_possiveis_artistas([melhor_item['artist']['name'] if melhor_item is not None else 'Desconhecido', musica.artista_titulo_filtrado])  
                musica.set_caminho(path)
                
                if melhor_score >= 0.85:
                    musica.set_status(SongStatus.ALTA)
                elif 0.85 > melhor_score > 0.65:
                    musica.set_status(SongStatus.MEDIA)
                else:
                    musica.set_status(SongStatus.BAIXA)

                if melhor_item is not None:

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
                                musica.path, 
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
                                musica.path, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        img_b_link = melhor_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.path, 
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
            {
                SongStatus.SEM_ART_FILTRADO : id3_only_list,
                SongStatus.SEM_ART_NATIVO : filtered_only_list
            }
        )
        Pipeline.executar_callbacks(path)

    @classmethod
    def _calcular_score_apenas_titulo(cls, musica : SongMetadata, item : dict):
        similaridade_titulo = Task.similaridade(
            musica.titulo_musica_filtrado.lower().strip(),
            item['title'].lower().strip()
        )            
        popularidade = item.get('rank', 0) / 1_000_000

        return (0.75 * similaridade_titulo + 0.15 * popularidade)
    
    @classmethod
    def _analisar_consenso(cls, itens):
        artistas = [i['artist']['name'] for i in itens[:5]]
        artista_dominante = max(set(artistas), key = artistas.count)
        frequencia = artistas.count(artista_dominante)
        consenso = frequencia / len(artistas)
        
        return consenso, artista_dominante
    
    @classmethod
    def _estrategia_apenas_titulo(cls):
        return {
            'artista_para_busca' : lambda musica: None,
            'calcular_score' : cls._calcular_score_apenas_titulo
        }
    
    @classmethod
    async def _classificar_artistas_apenas_titulo(cls, gap, sim_1, consenso, top5) -> str | SongStatus:
        artista = top5[0]["artist"]["name"]

        if sim_1 >= 0.85 and gap >= 0.05:
            return artista, SongStatus.ALTA
        elif sim_1 >= 0.80 and gap >= 0.02:
            return artista, SongStatus.MEDIA
        else:
            return artista, SongStatus.BAIXA
        
    @classmethod
    async def resolve_title_only(cls,  title_only_list : list[SongMetadata], path : str):
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)
            resultados_pipeline = []

            for musica in title_only_list:
                resultado = await fonts.deezer.buscar_musica(
                    titulo = musica.titulo_musica_filtrado,
                    artista = None
                )

                if not resultado or not resultado.get('track'):
                    musica.set_status(SongStatus.BAIXA)
                    musica.set_artista_final(None)
                    musica.set_artista_id(None)
                    musica.set_score(0)
                    continue

                itens = []

                for item in resultado['track']:
                    score = cls._calcular_score_apenas_titulo(musica = musica, item = item)
                    item['score_calculado'] = score
                    itens.append(item)
                
                itens_ordenados = sorted(
                    itens,
                    key = lambda x: x['score_calculado'],
                    reverse = True
                )

                possibilidades = [
                    {
                        'id' : item_ord['artist']['id'], 
                        'nome' : item_ord['artist']['name'], 
                        'score' : item_ord['score_calculado']
                    } for item_ord in itens_ordenados
                ]
                
                musica.set_possiveis_artistas(possibilidades)
                
                top5 = itens_ordenados[:5]
                sim_1 = top5[0]['score_calculado']
                sim_2 = top5[1]['score_calculado'] if len(top5) > 1 else 0
                gap = sim_1 - sim_2
                consenso, artista_dominante = cls._analisar_consenso(top5)

                artista_final, status_artista_final = await cls._classificar_artistas_apenas_titulo(
                    gap = gap, sim_1 = sim_1, consenso = consenso, top5 = top5
                )

                musica.set_artista_final(
                    Filtering._limpar_feat(artista_final)
                )
                musica.set_artista_id(
                    CacheArtists.resolver_id(
                        musica.artista_final
                    ) if musica.artista_final is not None else None
                ) 

                musica.set_consenso(consenso)
                musica.set_gap(gap)
                musica.set_sim_1(sim_1)
                musica.set_sim_2(sim_2)
                musica.set_status(status_artista_final)
                musica.set_caminho(path)

                caminho_img_medium_art = Persistencia.baixar_imagem(
                    url = top5[0]['artist']['picture_medium'],
                    caminho_destino = os.path.normpath(
                        os.path.join(
                            CAMINHO_ARTISTAS, 
                            musica.id_artista + '.jpg'
                        )
                    )
                )
                musica.set_imagem_artista(
                    id = top5[0]['artist']['id'] or None,
                    img_m = caminho_img_medium_art,
                    img_b = os.path.normpath(
                        os.path.join(
                            musica.path, 
                            musica.arquivo_mp3_original
                        )
                    ),
                    img_b_link = top5[0]['artist']['picture_big'] or None
                )
                
                caminho_img_medium_alb = Persistencia.baixar_imagem(
                    url = top5[0]['album']['cover_medium'],
                    caminho_destino = os.path.normpath(
                        os.path.join(
                            CAMINHO_ALBUNS, 
                            top5[0]['album']['title'] + '.jpg'
                        )
                    )
                )
                musica.set_imagem_album(
                    nome = top5[0]['album']['title'] or None,
                    id = top5[0]['album']['id'] or None,
                    img_m = caminho_img_medium_alb or None,
                    img_b = os.path.normpath(
                        os.path.join(
                            musica.path, 
                            musica.arquivo_mp3_original
                        )
                    ),
                    img_b_link = top5[0]['album']['cover_big'] or None
                )

                ExtractMetadata.registrar_metadados_player(
                        caminho_arquivo = os.path.normpath(
                            os.path.join(
                                musica.path, 
                                musica.arquivo_mp3_original
                            )
                        ),
                        titulo = musica.titulo_musica_filtrado if musica.titulo_musica_filtrado is not None else musica.arquivo_mp3_filtrado,
                        artista = musica.artista_final,
                        album = musica.img_album.get('nome'),
                        url_img_album_medium = top5[0]['album']['cover_medium'],
                        url_img_album_big = musica.img_album.get('big').get('link'),
                        url_img_artista_medium = top5[0]['artist']['picture_medium'],
                        url_img_artista_big = musica.img_artista.get('big').get('link'),
                        id_alb = musica.img_artista.get('id'),
                        id_art = musica.img_album.get('id')
                    )
                
        await Pipeline.salvar_dados(
            {SongStatus.APENAS_TITULO : title_only_list}
        )
        Pipeline.executar_callbacks(path)