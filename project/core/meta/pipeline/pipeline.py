# imports de back-end
from core.meta.enum.status import SongStatus, ScannerStatus
from core.meta.models.song import SongMetadata
from core.meta.pipeline.phase_1 import Phase1
from core.meta.pipeline.phase_2 import Phase2
from core.meta.pipeline.phase_3 import Phase3
from core.meta.repository.filtering import Filtering
from core.meta.repository.extract_metadata import ExtractMetadata
from core.meta.repository.metadata_repository import MetadataRepository
from core.meta.cache.cache_artists import CacheArtists
from core.meta.models.scanner_model import ScannerModel
from core.meta.scanner.scanner import Scanner
from core.meta.controller.scanner_controller import ScannerController
from core.playlists.controller.playlist_state import PlaylistState
from core.services.controllers.grid_state import GridState, GridMode
from core.playlists.enum.playlist_enum import PlaylistLoaded

# imports gerais
from pathlib import Path
import os, asyncio


class Pipeline:

    @classmethod
    async def _async_classificar_presenca(cls, filtered_title : dict[str | None], filtered_artist : str | None):
        if filtered_title is None:
            return SongStatus.INCOMPLETE

        if filtered_title['artist'] is not None and filtered_artist is None:
            return SongStatus.NO_ARTIST_ID3

        if filtered_title['artist'] is None and filtered_artist is not None:
            return SongStatus.NO_ARTIST_FILTERED

        if filtered_title['filtered_title'] is not None:
            return SongStatus.TITLE_ONLY

        return SongStatus.INCOMPLETE

    @classmethod
    def normalize_song(cls, song):
        if isinstance(song, SongMetadata):
            return song.mp3_file
        return song
    
    @classmethod
    async def save_data(cls, groups: dict):
        await MetadataRepository.data_manager_songs_json(groups = groups)
        await CacheArtists.save()
        await MetadataRepository.load_cache()
    
    @classmethod
    def to_execute_callbacks(cls, path: Path):
        GridState.notify(
            event = 'actualization_grid', 
            data = GridMode.ARTIST
        )
        GridState.notify(
            event = 'actualization_grid',
            data = GridMode.ALBUM
        )
        
        PlaylistState.notify(
            event = 'actualization_number_songs_of_playlist',
            data = {
                'id' : id,
                'qtde' : len(
                    os.listdir(path)
                )
            }
        )

        if (
            isinstance(PlaylistState.playlist_loaded, dict) and 
            PlaylistState.playlist_loaded['open'] == PlaylistLoaded.OPEN
        ):
            PlaylistState.notify(
                event = 'actualization_artist',
                data = None
            )
            PlaylistState.notify(
                event = 'actualization_cover',
                data = None
            )

    @classmethod
    def start_wrapper_sync(cls, path: str, object_list: list = [], id_playlist: str | None = None) -> list[SongMetadata]:
        
        ScannerModel.start_task()
        ScannerModel.set_status_prosesses(
            ScannerStatus.ON_PIPELINE_PLAYLIST
        )
        Scanner.manager_status()
        ScannerController.notify(
            'icon_status_scanner',
            None
        )

        try:
            asyncio.run(
                cls._async_processar_musica(
                    path = path, 
                    object_list = object_list,
                    id = id_playlist
                )
            )
        except Exception as e:
            import traceback

            print(f"[PIPELINE ERROR]: {e}")
            traceback.print_exc()
        finally:
            ScannerModel.finaly_task()
            
            if not ScannerModel.return_is_busy():
                ScannerModel.set_status_prosesses(
                    None
                )
                ScannerController.notify(
                    'progress_status_scanner',
                    None
                )
                Scanner.manager_status()
                
    @classmethod
    async def _async_processar_musica(
        cls, 
        path: Path, 
        object_list: list[SongMetadata] = [], 
        id: str | None = None
    ) -> list[SongMetadata]:

        list_already_processed: list[SongMetadata] = []
        lista = []
        
        song: SongMetadata | str
        for song in os.listdir(path) if len(object_list) == 0 else object_list:
            filtered_title = None
            filtered_artist = None

            song = cls.normalize_song(song)
            song = os.path.basename(song)

            destination_file = Path(path) / song
            # destination_file = os.path.normpath(
            #     os.path.join(path, song)
            # )

            # FASE 0 - verificação da existencia de data já alterados pelo próprio player, assim carregamento dos data já imbutidos.
            if ExtractMetadata.music_already_processed(destination_file):
                mus = ExtractMetadata.extract_metadata_playter(destination_file)
                
                artista_id = CacheArtists.resolve_id(mus.get('artist'))
                
                dic = await asyncio.to_thread(
                    ExtractMetadata.extact_images_mp3,
                    destination_file, 
                    mus, 
                    song.replace('.mp3', ''),
                    artista_id
                )
                
                list_already_processed.append(
                    SongMetadata(
                        playlist_id = id,
                        artist_id = artista_id,
                        song_title_id3_filtered = mus.get('title'),
                        defined_artist = mus.get('artist'),
                        mp3_file = song,
                        song_path = path,
                        mp3_file_title = None,
                        mp3_file_artist = None,
                        song_artist_id3_filtered = None,
                        consensus = None,
                        gap = None,
                        score = None,
                        sim_1 = None,
                        sim_2 = None,
                        list_of_potential_artists = [],
                        status = SongStatus.HIGH,
                        original_song_title = song,
                        album_metadata = {
                            'id_deezer' : mus.get('id_album'), 
                            'nome' : mus.get('album'), 
                            'medium' : dic.get('alb'), 
                            'big' : {
                                'link' : mus.get('imagem_album_player_big'),
                                'path' : destination_file
                            }
                        },
                        artist_metadata = {
                            'id_deezer' : mus.get('id_artista'), 
                            'medium' : dic.get('art'), 
                            'big' : {
                                'link' : mus.get('imagem_album_player_medium'),
                                'path' : destination_file
                            }
                        }
                    )
                )
            else:
                # FASE 1 - extração de metadados e classificação + filtragem tradicional
                data = await ExtractMetadata.async_extrair(destination_file)
                
                if data is not None:
                    if data['title'] is not None:
                        filtered_title = await Filtering.async_filter_title(nome = data['title'])

                    if data['artist'] is not None:
                        filtered_artist = await Filtering.async_filter_artist(artist = data['artist'])
                
                    if filtered_artist is not None and filtered_title['artist'] is not None:
                        lista.append(await Phase1.phase_1(
                            nome_arquivo_original = song,
                            filtered_title = filtered_title,
                            artista_meta_nativo = filtered_artist
                        ))
                    else:
                        lista.append(await ExtractMetadata.async_organiza_dados(
                            nome_arquivo_original = song,
                            filtered_title = filtered_title,
                            artista_meta_nativo = filtered_artist,
                            id_artista = '',
                            status = await cls._async_classificar_presenca(
                                filtered_title = filtered_title, 
                                filtered_artist = filtered_artist    
                            ),
                            id_playlist = id
                        ))
        
        group_phase_0 = {SongStatus.PHASE_0 : list_already_processed}
        await cls.save_data(groups = group_phase_0)
        cls.to_execute_callbacks(path)

        groups = await Phase2.phase_2(
            lista = lista, 
            path = path
        )
        
        await Phase3.phase_3(
            incomplete_list = groups[SongStatus.INCOMPLETE], 
            path = path
        )

        cls.to_execute_callbacks(path)