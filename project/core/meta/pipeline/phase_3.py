# imports de back-end
from core.meta.repository.filtering import Filtering
from core.meta.repository.tasks import Task
from core.meta.enum.status import SongStatus
from core.meta.provider.deezer import FontManager
from core.meta.models.song import SongMetadata
from core.meta.repository.metadata_repository import MetadataRepository
from core.services.account_manager import AccountManager
from core.meta.cache.cache_artists import CacheArtists
from core.meta.repository.extract_metadata import ExtractMetadata

# imports gerais
import aiohttp, os


class Phase3:

    @classmethod
    def _calculate_phase3_score_with_artist(cls, filter: dict, item: dict) -> float:
        return (
            0.6 * Task.similarity(
                filter["filtered_title"],
                item["title"]
            ) + 0.4 * Task.similarity(
                Filtering.clean_feat(filter["artist"]),
                item["artist"]["name"]
            )
        )
    
    @classmethod
    def _calculate_score_title_only_phase_3(cls, filter: dict, item: dict):
        title_similarity = Task.similarity(
            filter["filtered_title"].lower().strip(),
            item["title"].lower().strip()
        )
        polarity = item.get("rank", 0) / 1_000_000

        return (0.75 * title_similarity + 0.15 * polarity)
    
    @classmethod
    async def _sort_artists_by_title_only(cls, gap, sim_1, top5) -> str | SongStatus:
        artist = top5[0]["artist"]["name"]

        if sim_1 >= 0.85 and gap >= 0.05:
            return artist, SongStatus.HIGH
        elif sim_1 >= 0.80 and gap >= 0.02:
            return artist, SongStatus.MEDIUM
        else:
            return artist, SongStatus.LOW
        
    @classmethod
    async def _resolve_phase_3(cls, fonts: FontManager, filter: dict):
        result = await fonts.deezer.get_song(
            title = filter["filtered_title"],
            artist = filter["artist"]
        )

        if not result or not result.get("track"):
            return None, 0, None

        itens = result["track"]

        # 🔹 CASO 1: TEM ARTISTA NO FILENAME
        if filter["artist"]:
            best_item = None
            best_score = 0

            for item in itens:
                score = cls._calculate_phase3_score_with_artist(filter, item)

                if score > best_score:
                    best_score = score
                    best_item = item

            return best_item, best_score, None

        # 🔹 CASO 2: APENAS TÍTULO
        else:
            from core.meta.pipeline.phase_2 import Phase2
            
            processed_items = []

            for item in itens:
                score = cls._calculate_score_title_only_phase_3(filter, item)
                item["calculated_score"] = score
                processed_items.append(item)

            itens_ordenados = sorted(
                processed_items,
                key = lambda x: x["calculated_score"],
                reverse = True
            )

            top5 = itens_ordenados[:5]

            sim_1 = top5[0]["calculated_score"]
            sim_2 = top5[1]["calculated_score"] if len(top5) > 1 else 0
            gap = sim_1 - sim_2
            consensus, artista_dominante = Phase2.analyze_consensus(top5)

            defined_artist, status = await cls._sort_artists_by_title_only(
                gap = gap,
                sim_1 = sim_1,
                consensus = consensus,
                top5 = top5
            )

            return top5[0], sim_1, {
                "status": status,
                "gap": gap,
                "sim_1": sim_1,
                "sim_2": sim_2,
                "consensus": consensus,
                "defined_artist": defined_artist
            }
    
    @classmethod
    async def phase_3(cls, incomplete_list: list[SongMetadata], path: str):
        from core.meta.pipeline.pipeline import Pipeline

        CAMINHO_ARTISTAS = f"Assets/Data/Contas/{AccountManager.accounts_cache['current_account']}/Imagens/Artistas"
        CAMINHO_ALBUNS = f"Assets/Data/Contas/{AccountManager.accounts_cache['current_account']}/Imagens/Albuns"
        
        async with aiohttp.ClientSession() as session:
            fonts = FontManager(session)

            for song in incomplete_list:

                filter = await Filtering.async_filter_title(song.mp3_file)

                song.set_mp3_file_filtered(
                    title = filter["filtered_title"],
                    artist = filter["artist"]
                )
                song.set_song_path(path)
                
                if filter is None:
                    song.set_status(SongStatus.LOW)
                    song.set_score(0)
                    song.set_defined_artist(
                        Filtering.clean_feat(
                            best_item["artist"]["name"]
                        ) if best_item else Filtering.clean_feat(
                            filter["artist"]
                        ) or None
                    )  
                    song.set_artist_id(
                        CacheArtists.resolve_id(
                            song.defined_artist
                        ) if song.defined_artist is not None else None
                    )
                    continue

                best_item, best_score, title_only_data = await cls._resolve_phase_3(fonts, filter)

                if best_item is None:
                    song.set_status(SongStatus.LOW)
                    song.set_score(0)
                    song.set_defined_artist(
                        Filtering.clean_feat(
                            best_item["artist"]["name"]
                        ) if best_item else Filtering.clean_feat(
                            filter["artist"]
                        ) or None
                    )  
                    song.set_artist_id(
                        CacheArtists.resolve_id(
                            song.defined_artist
                        ) if song.defined_artist is not None else None
                    )
                    continue

                # 🔹 CASO APENAS TÍTULO
                if title_only_data:
                    song.set_defined_artist(
                        Filtering.clean_feat(
                            best_item["artist"]["name"]
                        ) if best_item else Filtering.clean_feat(
                            filter["artist"]
                        ) or None
                    )  
                    song.set_artist_id(
                        CacheArtists.resolve_id(
                            song.defined_artist
                        ) if song.defined_artist is not None else None
                    )
                    song.set_status(title_only_data["status"])
                    song.set_score(title_only_data["sim_1"])
                    song.set_gap(title_only_data["gap"])
                    song.set_sim_1(title_only_data["sim_1"])
                    song.set_sim_2(title_only_data["sim_2"])
                    song.set_consensus(title_only_data["consensus"])
                    
                    artist_image_medium_destination = MetadataRepository.download_image(
                        url = best_item["artist"]["picture_medium"],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                song.artist_id + ".jpg"
                            )
                        )
                    )
                    song.set_artist_metadata(
                        id_deezer = best_item["artist"]["id_deezer"] or None,
                        img_m = artist_image_medium_destination,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item["artist"]["picture_big"] or None
                    )
                    
                    album_image_medium_destination = MetadataRepository.download_image(
                        url = best_item["album"]["cover_medium"],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                best_item["album"]["title"] + ".jpg"
                            )
                        )
                    )
                    song.set_album_metadata(
                        name = best_item["album"]["title"] or None,
                        id_deezer = best_item["album"]["id_deezer"] or None,
                        img_m = album_image_medium_destination or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item["album"]["cover_big"] or None
                    )

                    ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("title") if song.id3_data is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get("name"),
                        url_img_album_medium = best_item["album"]["cover_medium"],
                        url_img_album_big = song.album_metadata.get("big").get("link"),
                        url_img_artista_medium = best_item["artist"]["picture_medium"],
                        url_img_artista_big = song.artist_metadata.get("big").get("link"),
                        id_alb = song.artist_metadata.get("id_deezer"),
                        id_art = song.album_metadata.get("id_deezer")
                    )
                # 🔹 CASO COM ARTISTA
                else:
                    from core.meta.pipeline.phase_2 import Phase2

                    defined_artist = await Phase2.choose_artist(
                        score = best_score,
                        best_item = best_item,
                        song = song
                    )

                    song.set_defined_artist(
                        Filtering.clean_feat(
                            best_item["artist"]["name"]
                        ) if best_item else Filtering.clean_feat(
                            filter["artist"]
                        ) or None
                    )  
                    song.set_artist_id(
                        CacheArtists.resolve_id(
                            song.defined_artist
                        ) if song.defined_artist is not None else None
                    )

                    song.set_score(best_score)

                    if best_score >= 0.85:
                        song.set_status(SongStatus.HIGH)
                    elif 0.85 > best_score > 0.65:
                        song.set_status(SongStatus.MEDIUM)
                    else:
                        song.set_status(SongStatus.LOW)       

                    artist_image_medium_destination = MetadataRepository.download_image(
                        url = best_item["artist"]["picture_medium"],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ARTISTAS, 
                                song.artist_id + ".jpg"
                            )
                        )
                    )
                    song.set_artist_metadata(
                        id_deezer = best_item["artist"]["id_deezer"] or None,
                        img_m = artist_image_medium_destination,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item["artist"]["picture_big"] or None
                    )
                    
                    album_image_medium_destination = MetadataRepository.download_image(
                        url = best_item["album"]["cover_medium"],
                        caminho_destino = os.path.normpath(
                            os.path.join(
                                CAMINHO_ALBUNS, 
                                best_item["album"]["title"] + ".jpg"
                            )
                        )
                    )
                    song.set_imagem_album(
                        name = best_item["album"]["title"] or None,
                        id_deezer = best_item["album"]["id_deezer"] or None,
                        img_m = album_image_medium_destination or None,
                        img_b = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        img_b_link = best_item["album"]["cover_big"] or None
                    )

                    ExtractMetadata.register_metadata_player(
                        file_path = os.path.normpath(
                            os.path.join(
                                song.song_path, 
                                song.mp3_file
                            )
                        ),
                        title = song.id3_data["filtered_data"].get("title") if song.id3_data is not None else song.mp3_file_filtered.get("title"),
                        artist = song.defined_artist,
                        album = song.album_metadata.get("name"),
                        url_img_album_medium = best_item["album"]["cover_medium"],
                        url_img_album_big = song.album_metadata.get("big").get("link"),
                        url_img_artista_medium = best_item["artist"]["picture_medium"],
                        url_img_artista_big = song.artist_metadata.get("big").get("link"),
                        id_alb = song.artist_metadata.get("id_deezer"),
                        id_art = song.album_metadata.get("id_deezer")
                    )

        await Pipeline.save_data({
            SongStatus.INCOMPLETE : incomplete_list
        })
        Pipeline.to_execute_callbacks(path)