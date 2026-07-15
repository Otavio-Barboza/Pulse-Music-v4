# imports de back-end
from project.core.meta.repository.filtering import Filtering
from project.core.meta.repository.tasks import Task
from project.core.meta.enum.status import SongStatus
from project.core.meta.provider.deezer import FontManager
from project.core.meta.models.song import SongMetadata
from project.core.meta.repository.extract_metadata import ExtractMetadata
from project.core.meta.cache.cache_artists import CacheArtists
from project.core.meta.repository.metadata_repository import MetadataRepository
from project.core.services.account_manager import AccountManager       

# imports gerais
from pathlib import Path
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
            both_list = groups[SongStatus.BOTH], 
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
    async def resolve_both(cls, both_list : list[SongMetadata], path : str):
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)
            
            for song in both_list:
                song.set_defined_artist(
                    Filtering.clean_feat(
                        song.id3_data["filtered_data"].get("song_artist_id3_filtered")
                    )
                )
                song.set_artist_id(
                    CacheArtists.resolve_id(
                        song.defined_artist
                    ) if song.defined_artist is not None else None
                )
                song.set_potential_artists([song.id3_data["original_data"].get("original_artist_id3")])
                song.set_status(SongStatus.HIGH)
                song.set_score(1.5)
                song.set_song_path(path)
                
                deezer_data = await fonts.deezer.get_song(
                    title = song.id3_data["filtered_data"].get("song_title_id3_filtered"), artist = song.defined_artist
                )
                
                image_medium_artist_destination = MetadataRepository.download_image(
                    url = deezer_data['track'][0]['artist']['picture_medium'],
                    destination_path = os.path.normpath(
                        os.path.join(
                            CAMINHO_ARTISTAS, 
                            song.artist_id + '.jpg'
                        )
                    )
                )
                song.set_artist_metadata(
                    id_deezer = deezer_data['track'][0]['artist']['id_deezer'] or None,
                    img_m = image_medium_artist_destination,
                    img_b = os.path.normpath(
                        os.path.join(
                            song.path, 
                            song.mp3_file
                        )
                    ),
                    img_b_link = deezer_data['track'][0]['artist']['picture_big'] or None
                )

                image_medium_album_destination = MetadataRepository.download_image(
                    url = deezer_data['track'][0]['album']['cover_medium'],
                    destination_path = os.path.normpath(
                        os.path.join(
                            CAMINHO_ALBUNS, 
                            deezer_data['track'][0]['album']['title'] + '.jpg'
                        )
                    )
                )
                song.set_album_metadata(
                    name = deezer_data['track'][0]['album']['title'] or None,
                    id_deezer = deezer_data['track'][0]['album']['id_deezer'] or None,
                    img_m = image_medium_album_destination or None,
                    img_b = os.path.normpath(
                        os.path.join(
                            song.path, 
                            song.mp3_file
                        )
                    ),
                    img_b_link = deezer_data['track'][0]['album']['cover_big'] or None
                )

                ExtractMetadata.register_metadata_player(
                    file_path = os.path.normpath(
                        os.path.join(
                            song.path, 
                            song.mp3_file
                        )
                    ),
                    title = song.id3_data["filtered_data"].get("song_title_id3_filtered") if song.id3_data["filtered_data"].get("song_title_id3_filtered") is not None else song.mp3_file_filtered.get("title"),
                    artist = song.defined_artist,
                    album = song.album_metadata.get('name'),
                    url_img_album_medium = deezer_data['track'][0]['album']['cover_medium'],
                    url_img_album_big = song.album_metadata.get('big').get('link'),
                    url_img_artista_medium = deezer_data['track'][0]['artist']['picture_medium'],
                    url_img_artista_big = song.artist_metadata.get('big').get('link'),
                    id_alb = song.artist_metadata.get('id_deezer'),
                    id_art = song.album_metadata.get('id_deezer')
                )

        await Pipeline.save_data({SongStatus.BOTH : both_list})
        Pipeline.to_execute_callbacks(path)
    
    @classmethod
    async def resolve_song(
        cls, 
        fonts: FontManager, 
        song: SongMetadata, 
        strategy: dict
    ):
        artist_for_search = strategy['artist_for_search'](song)

        result = await fonts.deezer.get_song(
            title = song.id3_data["filtered_data"].get("song_title_id3_filtered"),
            artist = artist_for_search
        )

        if not result.get('track'):
            return None, 0
        
        best_item = None
        best_score = 0

        for item in result['track']:
            score = strategy['calculate_score'](song, item)

            if score > best_score:
                best_score = score
                best_item = item
        
        return best_item, best_score
    
    @classmethod
    async def choose_artist(
        cls, 
        score: float, 
        best_item: dict, 
        song: SongMetadata
    ):
        if score >= 0.85:
            return best_item['artist']['name']
        elif 0.85 > score > 0.65:
            return song.id3_data["filtered_data"].get("song_artist_id3_filtered") or song.id3_data["original_data"].get("original_artist_id3")
        else:
            return song.id3_data["original_data"].get("original_artist_id3") or song.id3_data["filtered_data"].get("song_artist_id3_filtered")
        
    @classmethod
    def _medium_strategy(cls):
        return {
            'artist_for_search' : lambda song: Filtering.clean_feat(song.id3_data["filtered_data"].get("song_artist_id3_filtered")),
            'calculate_score' : lambda song, item: (
                0.6 * Task.similarity(
                    song.id3_data["filtered_data"].get("song_title_id3_filtered"),
                    item['title']
                ) + 0.4 * max(
                    Task.similarity(
                        Filtering.clean_feat(song.id3_data["filtered_data"].get("song_artist_id3_filtered")),
                        item['artist']['name']
                    ),
                    Task.similarity(
                        song.id3_data["original_data"].get("original_artist_id3"),
                        item['artist']['name']
                    )
                )
            )
        }
    
    @classmethod
    async def resolve_medium_and_inconsistent(
        cls, 
        medium_list: list[SongMetadata], 
        inconsitent_list: list[SongMetadata], 
        path: Path
    ):
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)

            for song in medium_list:
                best_item, best_score = await cls.resolve_song(
                    song = song,
                    fonts = fonts,
                    strategy = cls._medium_strategy()
                )
                defined_artist = await cls.choose_artist(
                    score = best_score,
                    best_item = best_item,
                    song = song
                )

                song.set_defined_artist(
                    Filtering.clean_feat(defined_artist)
                )
                song.set_artist_id(
                    CacheArtists.resolve_id(
                        song.defined_artist
                    ) if song.defined_artist is not None else None
                )

                song.set_score(best_score)
                song.set_potential_artists(
                    [
                        best_item['artist']['name'] if best_item is not None else 'Desconhecido', 
                        song.id3_data["filtered_data"].get("song_artist_id3_filtered"),
                        song.id3_data["original_data"].get("original_artist_id3")
                    ]
                )  
                song.set_song_path(path)
                
                if best_score >= 0.85:
                    song.set_status(SongStatus.HIGH)
                elif 0.85 > best_score > 0.65:
                    song.set_status(SongStatus.MEDIUM)
                else:
                    song.set_status(SongStatus.LOW)

                if best_item is not None:

                    image_medium_artist_destination = MetadataRepository.download_image(
                        url = best_item['artist']['picture_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                song.artist_id + '.jpg'
                            )
                        )
                    )
                    song.set_artist_metadata(
                        id_deezer = best_item['artist']['id_deezer'] or None,
                        img_m = image_medium_artist_destination,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['artist']['picture_big'] or None
                    )
                    
                    image_medium_album_destination = MetadataRepository.download_image(
                        url = best_item['album']['cover_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                best_item['album']['title'] + '.jpg'
                            )
                        )
                    )
                    song.set_album_metadata(
                        name = best_item['album']['title'] or None,
                        id_deezer = best_item['album']['id_deezer'] or None,
                        img_m = image_medium_album_destination or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("song_title_id3_filtered") if song.id3_data["filtered_data"].get("song_title_id3_filtered") is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get('name'),
                        url_img_album_medium = best_item['album']['cover_medium'],
                        url_img_album_big = song.album_metadata.get('big').get('link'),
                        url_img_artista_medium = best_item['artist']['picture_medium'],
                        url_img_artista_big = song.artist_metadata.get('big').get('link'),
                        id_alb = song.artist_metadata.get('id_deezer'),
                        id_art = song.album_metadata.get('id_deezer')
                    )

            for song in inconsitent_list:
                best_item, best_score = await cls.resolve_song(
                    song = song,
                    fonts = fonts,
                    strategy = cls._medium_strategy()
                )
                defined_artist = await cls.choose_artist(
                    score = best_score,
                    best_item = best_item,
                    song = song
                )

                song.set_defined_artist(
                    Filtering.clean_feat(defined_artist)
                )
                song.set_artist_id(
                    CacheArtists.resolve_id(
                        song.defined_artist
                    ) if song.defined_artist is not None else None
                )

                song.set_score(best_score)
                song.set_potential_artists([best_item['artist']['name'] if best_item is not None else 'Desconhecido', song.id3_data["filtered_data"].get("song_artist_id3_filtered"), song.id3_data["original_data"].get("original_artist_id3")])
                song.set_song_path(path)

                if best_score >= 0.85:
                    song.set_status(SongStatus.HIGH)
                elif 0.85 > best_score > 0.65:
                    song.set_status(SongStatus.MEDIUM)
                else:
                    song.set_status(SongStatus.LOW)

                if best_item is not None:

                    image_medium_artist_destination =  MetadataRepository.download_image(
                        url = best_item['artist']['picture_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                song.artist_id + '.jpg'
                            )
                        )   
                    )
                    song.set_artist_metadata(
                        id_deezer = best_item['artist']['id_deezer'] or None,
                        img_m = image_medium_artist_destination,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['artist']['picture_big'] or None
                    )
                    
                    image_medium_album_destination = MetadataRepository.download_image(
                        url = best_item['album']['cover_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                best_item['album']['title'] + '.jpg'
                            )
                        )
                    )
                    song.set_album_metadata(
                        name = best_item['album']['title'] or None,
                        id_deezer = best_item['album']['id_deezer'] or None,
                        img_m = image_medium_album_destination or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("song_title_id3_filtered") if song.id3_data["filtered_data"].get("song_title_id3_filtered") is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get('name'),
                        url_img_album_medium = best_item['album']['cover_medium'],
                        url_img_album_big = song.album_metadata.get('big').get('link'),
                        url_img_artista_medium = best_item['artist']['picture_medium'],
                        url_img_artista_big = song.artist_metadata.get('big').get('link'),
                        id_alb = song.artist_metadata.get('id_deezer'),
                        id_art = song.album_metadata.get('id_deezer')
                    )
        
        await Pipeline.salvar_dados(
            {
                SongStatus.MEDIO : medium_list,
                SongStatus.INCONSISTENTE : inconsitent_list
            }
        )
        Pipeline.to_execute_callbacks(path)

    @classmethod
    def _estrategia_artista_filtrado(cls):
        return {
            'artist_for_search' : lambda song: Filtering.clean_feat(song.id3_data["filtered_data"].get("song_artist_id3_filtered")),
            'calculate_score' : lambda song, item: (
                0.6 * Task.similarity(
                    song.id3_data["filtered_data"].get("song_title_id3_filtered"),
                    item['title']
                ) + 0.4 * Task.similarity(
                    song.id3_data["filtered_data"].get("song_artist_id3_filtered"),
                    item['artist']['name']
                )
            )
        }
    
    @classmethod
    def _estrategia_artista_nativo(cls):
        return {
            'artist_for_search' : lambda song: song.id3_data["original_data"].get("original_artist_id3"),
            'calculate_score' : lambda song, item: (
                0.6 * Task.similarity(
                    song.id3_data["filtered_data"].get("song_title_id3_filtered"),
                    item['title']
                ) + 0.4 * Task.similarity(
                    song.id3_data["original_data"].get("original_artist_id3"),
                    item['artist']['name']
                )
            )
        }
    
    @classmethod
    async def resolve_no_artist_filtered_or_no_id3(cls, id3_only_list : list[SongMetadata], filtered_only_list : list[SongMetadata], path : str):
        from .pipeline import Pipeline
        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)
            lista = []

            for song in filtered_only_list:
                best_item, best_score = await cls.resolve_song(
                    fonts = fonts,
                    song = song,
                    strategy = cls._estrategia_artista_filtrado()
                )
                defined_artist = await cls.choose_artist(
                    score = best_score,
                    best_item = best_item,
                    song = song
                )

                song.set_defined_artist(
                    Filtering.clean_feat(defined_artist)
                )
                song.set_artist_id(
                    CacheArtists.resolve_id(
                        song.defined_artist
                    ) if song.defined_artist is not None else None
                )

                song.set_score(best_score)
                song.set_potential_artists(
                    [
                        best_item['artist']['name'] if best_item is not None else 'Desconhecido', 
                        song.id3_data["original_data"].get("original_artist_id3")
                    ]
                )  
                song.set_song_path(path)
                
                if best_score >= 0.85:
                    song.set_status(SongStatus.HIGH)
                elif 0.85 > best_score > 0.65:
                    song.set_status(SongStatus.MEDIUM)
                else:
                    song.set_status(SongStatus.LOW)

                if best_item is not None:

                    image_medium_artist_destination = MetadataRepository.download_image(
                        url = best_item['artist']['picture_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                song.artist_id + '.jpg'
                            )
                        )
                    )
                    song.set_artist_metadata(
                        id_deezer = best_item['artist']['id_deezer'] or None,
                        img_m = image_medium_artist_destination,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['artist']['picture_big'] or None
                    )
                    
                    image_medium_album_destination = MetadataRepository.download_image(
                        url = best_item['album']['cover_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                best_item['album']['title'] + '.jpg'
                            )
                        )
                    )
                    song.set_album_metadata(
                        name = best_item['album']['title'] or None,
                        id_deezer = best_item['album']['id_deezer'] or None,
                        img_m = image_medium_album_destination or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("song_title_id3_filtered") if song.id3_data["filtered_data"].get("song_title_id3_filtered") is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get('name'),
                        url_img_album_medium = best_item['album']['cover_medium'],
                        url_img_album_big = song.album_metadata.get('big').get('link'),
                        url_img_artista_medium = best_item['artist']['picture_medium'],
                        url_img_artista_big = song.artist_metadata.get('big').get('link'),
                        id_alb = song.artist_metadata.get('id_deezer'),
                        id_art = song.album_metadata.get('id_deezer')
                    )

            for song in id3_only_list:
                best_item, best_score = await cls.resolve_song(
                    fonts = fonts,
                    song = song,
                    strategy = cls._estrategia_artista_nativo()
                )
                defined_artist = await cls.choose_artist(
                    score = best_score,
                    best_item = best_item,
                    song = song
                )

                song.set_defined_artist(
                    Filtering.clean_feat(defined_artist)
                )
                song.set_artist_id(
                    CacheArtists.resolve_id(
                        song.defined_artist
                    ) if song.defined_artist is not None else None
                )

                song.set_score(best_score)
                song.set_potential_artists(
                    [
                        best_item['artist']['name'] if best_item is not None else 'Desconhecido', 
                        song.id3_data["filtered_data"].get("song_artist_id3_filtered")
                    ]
                )  
                song.set_song_path(path)
                
                if best_score >= 0.85:
                    song.set_status(SongStatus.HIGH)
                elif 0.85 > best_score > 0.65:
                    song.set_status(SongStatus.MEDIUM)
                else:
                    song.set_status(SongStatus.LOW)

                if best_item is not None:

                    image_medium_artist_destination = MetadataRepository.download_image(
                        url = best_item['artist']['picture_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                song.artist_id + '.jpg'
                            )
                        )
                    )
                    song.set_artist_metadata(
                        id_deezer = best_item['artist']['id_deezer'] or None,
                        img_m = image_medium_artist_destination,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['artist']['picture_big'] or None
                    )
                    
                    image_medium_album_destination = MetadataRepository.download_image(
                        url = best_item['album']['cover_medium'],
                        destination_path = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                best_item['album']['title'] + '.jpg'
                            )
                        )
                    )
                    song.set_album_metadata(
                        name = best_item['album']['title'] or None,
                        id_deezer = best_item['album']['id_deezer'] or None,
                        img_m = image_medium_album_destination or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item['album']['cover_big'] or None
                    )

                    ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("song_title_id3_filtered") if song.id3_data["filtered_data"].get("song_title_id3_filtered") is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get('name'),
                        url_img_album_medium = best_item['album']['cover_medium'],
                        url_img_album_big = song.album_metadata.get('big').get('link'),
                        url_img_artista_medium = best_item['artist']['picture_medium'],
                        url_img_artista_big = song.artist_metadata.get('big').get('link'),
                        id_alb = song.artist_metadata.get('id_deezer'),
                        id_art = song.album_metadata.get('id_deezer')
                    )

        await Pipeline.save_data(
            {
                SongStatus.NO_ARTIST_FILTERED : id3_only_list,
                SongStatus.NO_ARTIST_ID3 : filtered_only_list
            }
        )
        Pipeline.to_execute_callbacks(path)

    @classmethod
    def _calculate_score_title_only(cls, song: SongMetadata, item: dict):
        similarity_title = Task.similarity(
            song.id3_data["filtered_data"].get("song_title_id3_filtered").lower().strip(),
            item['title'].lower().strip()
        )            
        popularity = item.get('rank', 0) / 1_000_000

        return (0.75 * similarity_title + 0.15 * popularity)
    
    @classmethod
    def analyze_consensus(cls, itens):
        artist = [i['artist']['name'] for i in itens[:5]]
        dominant_artist = max(set(artist), key = artist.count)
        frequency = artist.count(dominant_artist)
        consensus = frequency / len(artist)
        
        return consensus, dominant_artist
    
    @classmethod
    def _strategy_title_only(cls):
        return {
            'artist_for_search' : lambda song: None,
            'calculate_score' : cls._calculate_score_title_only
        }
        
    @classmethod
    async def resolve_title_only(cls,  title_only_list: list[SongMetadata], path: Path):
        from .pipeline import Pipeline

        CAMINHO_ARTISTAS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Artistas'
        CAMINHO_ALBUNS = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Imagens/Albuns'
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)

            for song in title_only_list:
                result = await fonts.deezer.get_song(
                    title = song.id3_data["filtered_data"].get("song_title_id3_filtered"),
                    artist = None
                )

                if not result or not result.get('track'):
                    song.set_status(SongStatus.LOW)
                    song.set_defined_artist(None)
                    song.set_artist_id(None)
                    song.set_score(0)
                    continue

                itens = []

                for item in result['track']:
                    score = cls._calculate_score_title_only(song = song, item = item)
                    item['score_calculado'] = score
                    itens.append(item)
                
                ordered_itens = sorted(
                    itens,
                    key = lambda x: x['score_calculado'],
                    reverse = True
                )

                possibilities = [
                    {
                        'id_deezer' : item_ord['artist']['id_deezer'], 
                        'name' : item_ord['artist']['name'], 
                        'score' : item_ord['score_calculado']
                    } for item_ord in ordered_itens
                ]
                
                song.set_potential_artists(possibilities)
                
                top5 = ordered_itens[:5]
                sim_1 = top5[0]['score_calculado']
                sim_2 = top5[1]['score_calculado'] if len(top5) > 1 else 0
                gap = sim_1 - sim_2
                consensus, dominant_artist = cls.analyze_consensus(top5)

                defined_artist, status_artista_final = await cls._classificar_artistas_apenas_titulo(
                    gap = gap, sim_1 = sim_1, consensus = consensus, top5 = top5
                )

                song.set_defined_artist(
                    Filtering.clean_feat(defined_artist)
                )
                song.set_artist_id(
                    CacheArtists.resolve_id(
                        song.defined_artist
                    ) if song.defined_artist is not None else None
                ) 

                song.set_consenso(consensus)
                song.set_gap(gap)
                song.set_sim_1(sim_1)
                song.set_sim_2(sim_2)
                song.set_status(status_artista_final)
                song.set_song_path(path)

                image_medium_artist_destination = MetadataRepository.download_image(
                    url = top5[0]['artist']['picture_medium'],
                    destination_path = os.path.normpath(
                        os.path.join(
                            CAMINHO_ARTISTAS, 
                            song.artist_id + '.jpg'
                        )
                    )
                )
                song.set_artist_metadata(
                    id_deezer = top5[0]['artist']['id_deezer'] or None,
                    img_m = image_medium_artist_destination,
                    img_b = os.path.normpath(
                        os.path.join(
                            song.song_path, 
                            song.mp3_file
                        )
                    ),
                    img_b_link = top5[0]['artist']['picture_big'] or None
                )
                
                image_medium_album_destination = MetadataRepository.download_image(
                    url = top5[0]['album']['cover_medium'],
                    destination_path = os.path.normpath(
                        os.path.join(
                            CAMINHO_ALBUNS, 
                            top5[0]['album']['title'] + '.jpg'
                        )
                    )
                )
                song.set_album_metadata(
                    name = top5[0]['album']['title'] or None,
                    id_deezer = top5[0]['album']['id_deezer'] or None,
                    img_m = image_medium_album_destination or None,
                    img_b = os.path.normpath(
                        os.path.join(
                            song.song_path, 
                            song.mp3_file
                        )
                    ),
                    img_b_link = top5[0]['album']['cover_big'] or None
                )

                ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("song_title_id3_filtered") if song.id3_data["filtered_data"].get("song_title_id3_filtered") is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get('name'),
                        url_img_album_medium = top5[0]['album']['cover_medium'],
                        url_img_album_big = song.album_metadata.get('big').get('link'),
                        url_img_artista_medium = top5[0]['artist']['picture_medium'],
                        url_img_artista_big = song.artist_metadata.get('big').get('link'),
                        id_alb = song.artist_metadata.get('id_deezer'),
                        id_art = song.album_metadata.get('id_deezer')
                    )
                
        await Pipeline.salvar_dados(
            {SongStatus.TITLE_ONLY : title_only_list}
        )
        Pipeline.to_execute_callbacks(path)