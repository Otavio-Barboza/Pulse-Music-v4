# ESTRUTURA DA FASE 2


## Objetivo

Resolver os metadados classificados pela Fase 1, encaminhando cada grupo para o resolver adequado.


## Arquivos:

    ( project\core\meta\pipeline\phase2 ) : {
        
        phase_2.py,

        resolvers/
            resolver.py
            both.py
            medium_and_inconsitent.py
            no_artist_filtered_or_no_id3.py
            title_only.py
    }


## Dependências Diretas:

    Repositório (repository):

        ( project\core\meta\repository\filtering.py ) : {
            Filtering [class]
        }

        ( project\core\meta\repository\extract_metadata.py ) : {
            ExtractMetadata [class]
        }

        ( project\core\meta\repository\metadata_repository.py ) : {
            MetadataRepository [class]
        }

        ( project\core\meta\repository\filtering.py ) : {
            Filtering [class]
        }


    Cache:

        ( project\core\meta\cache\cache_artists.py ) : {
            CacheArtists [class]
        } 


    Models:

        ( project\core\meta\models\song.py ) : {
            SongMetadata [class]
        }


    Enum:

        ( project\core\meta\enum\status.py ) : {
            SongStatus [class : enum]
        }

    
    Provedores (provider) :
        
        ( project\core\meta\provider\deezer.py ) : {
            FontManager [class]
        }


    Serviços (services):

        ( project\core\services\account_manager.py ) : {
            AccountManager [class]
        }


    Utilidades (utils):

        ( project\core\utils\path.py ) : {
            AppPaths [class]
        }


## Fluxo de Execução:

    Criação do dicionário "groups", responsável por separar os objetos SongMetada conforme a classificação recebida da Fase 1.
    
        ↓
    
    Cada SongMetadata é adicionado à lista correspondente.
    
        ↓

    Cada grupo é enviado ao resolver especificamente cada classificação, sendo as:

        1. BOTH (ambos);
        2. MEDIM and INCONSISTENT (medios e inconsistentes);
        3. NO ARTIST FILTERED or NO ID3 (sem artista filtrado ou sem artista nativo [id3]);
        4. TITLE ONLY (apenas título).
