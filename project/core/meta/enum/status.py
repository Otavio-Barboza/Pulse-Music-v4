# import geral
from enum import Enum


class SongStatus(str, Enum):

    # ambos
    BOTH = 'both'
    
    # medio ou leve desconfiança
    SLIGHT_SUSPICION = 'slight_suspicion'
    
    # músicas com inconsistências relevantes
    INCONSISTENT = 'inconsistent'

    # não contém o artista id3 de metadado original, mas contém artista filtrado
    NO_ARTIST_ID3 = 'no_artist_id3'

    # inverso do ID3
    NO_ARTIST_FILTERED = 'no_artist_filtered'
    
    # apenas titulo (não contém nenhum tipo de artista identificado) e incompleto
    TITLE_ONLY = 'title_only'
    INCOMPLETE = 'incomplete'

    # confiança artistas
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    PHASE_0 = 'phase_0'


class ScannerStatus(str, Enum):
    
    PAUSE = 'pause'
    ON = 'on'
    BREAK = 'break' 
    
    ON_SCANNER = 'on_scanner'
    ON_PIPELINE_PLAYLIST = 'on_pipeline_playlist'