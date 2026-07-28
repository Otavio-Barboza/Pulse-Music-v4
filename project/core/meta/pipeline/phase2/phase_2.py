# imports de back-end
from core.meta.enum.status import SongStatus
from core.meta.models.song import SongMetadata
from core.meta.pipeline.phase2.resolvers.both import resolve_both
from core.meta.pipeline.phase2.resolvers.medium_and_inconsistent import resolve_medium_and_inconsistent
from core.meta.pipeline.phase2.resolvers.no_artist_filtered_or_no_id3 import resolve_no_artist_filtered_or_no_id3
from core.meta.pipeline.phase2.resolvers.title_only import resolve_title_only

# imports gerais
from pathlib import Path
import aiohttp, os


class Phase2:

    """  função coordenadora do fluxo  """

    @classmethod
    async def phase_2(cls, list_object: list[SongMetadata], path: str) -> dict[SongStatus, list[SongMetadata]]:
        """
        _summary_: Esta função vai orquestrar o fluxo das operações (
            BOTH -> MEDIUM -> INCONSISTENT -> INCOMPLETE -> TITLE_ONLY -> NO_ARTIST_FILTERED -> NO_ARTIST_ID3
        ). Essas operações possuem as suas resoluções separadas uma por uma e cada uma com a sua estratégia.

        Args:
            _list_object (list[SongMetadata]): Lista de objetos SongMetadata que são ser editados conforme as resuluções de cada um.
            _path (str): caminho das músicas.
        
        Returns:
            dict[SongStatus, list[SongMetadata]]: dicionários definidos com listas de objetos SongMetadata trabalhados separados todos com suas classificações (nesse caso cada classificação refere-se a uma chave e o value a lista de objetos tratadado da respectiva chave/classficação).
        """

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

        await resolve_both(
            both_list = groups[SongStatus.BOTH], 
            path = path
        )
        await resolve_medium_and_inconsistent(
            inconsitent_list = groups[SongStatus.INCONSISTENT],
            medium_list = groups[SongStatus.MEDIUM],
            path = path
        )
        await resolve_no_artist_filtered_or_no_id3(
            filtered_only_list = groups[SongStatus.NO_ARTIST_ID3],
            id3_only_list = groups[SongStatus.NO_ARTIST_FILTERED],
            path = path
        )
        await resolve_title_only(
            title_only_list = groups[SongStatus.TITLE_ONLY],
            path = path
        )

        return groups