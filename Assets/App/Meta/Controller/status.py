from enum import Enum

class Status(str, Enum):
    AMBOS = 'ambos'
    MEDIO = 'medio'
    INCONSISTENTE = 'inconsistente'
    SEM_ART_NATIVO = 'sem-art-nativo'
    SEM_ART_FILTRADO = 'sem-art-filtrado'
    APENAS_TITULO = 'apenas-titulo'
    INCOMPLETO = 'incompleto'

    # confiança artistas
    ALTA = 'alta'
    MEDIA = 'media'
    BAIXA = 'baixa'
    METADADOS_FASE_0 = 'fase-0'

class StatusScanner(str, Enum):
    PAUSE = 'pause'
    ON = 'on'
    BREAK = 'break' 
    
    ON_SCANNER = 'on_scanner'
    ON_PIPELINE_PLAYLIST = 'on_pipeline_playlist'