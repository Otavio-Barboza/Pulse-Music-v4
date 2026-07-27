# OPERAÇÃO DO PIPELINE: ARQUIVOS, RESPONSABILIDADES E DEPEDÊNCIAS.


# Arquivos:

    pipeline.md:
        - Fluxo geral do pipeline;
        - Orquestrador das execuções do inicio ao fim.


    phase_1.md:
        - Classificação inicial dos metadados.


    phase_2.md:
        - Resolução utilizando ID3 e Deezer.


    phase_3.md:
        - Resolução baseada no filename (nome integral do arquivo .mp3).


# Dependências:

    (project\core\meta\repository\filtering) : {
        Filtering
    }

    (project\core\meta\repository\extract_metadata) : {
        ExtractMetadata
    }

    (project\core\meta\repository\metadata_repository.py) : {
        MetadataRepository
    }

    (project\core\meta\cache\cache_artists.py) : {
        CacheArtists
    } 

    (project\core\meta\models\song.py) : {
        SongMetadata
    }