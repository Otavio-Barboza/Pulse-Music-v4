# ESTRUTURA DO PIPELINE


## Objetivos:

Orquestrar o processo de captação e gerenciamento de metadados divididos pelas fases 0, 1, 2 e 3.


## Arquivos:
    
    ( project\core\meta\pipeline ) : {   
        pipeline.py
    }


## Dependências Diretas:

    Pipeline:
    
        ( project\core\meta\pipeline\phase_1.py ) : {   
            Phase1 [class]
        }

        ( project\core\meta\pipeline\phase2\phase_2.py ) : {   
            Phase2 [class]
        }

        ( project\core\meta\pipeline\phase_3.py ) : {   
            Phase3 [class]
        }


    Modelos (models):

        ( project\core\meta\models\song.py ) : {   
            SongMetadata [class]
        }

        ( project\core\meta\models\scanner_model.py ) : {   
            ScannerModel [class]
        }


    Enum:

        ( project\core\meta\enum\status.py ) : {   
            SongStatus [class : enum], 
            ScannerStatus [class : enum]
        }

        ( project\core\playlists\enum\playlist_enum.py ) : {   
            PlaylistLoaded [class : enum]
        }


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


    Cache:

        ( project\core\meta\cache\cache_artists.py ) : {   
            CacheArtists [class]
        }


    Controllers:

        ( project\core\meta\scanner\scanner.py ) : {   
            Scanner [class]
        }

        ( project\core\meta\controller\scanner_controller.py ) : {   
            ScannerController [class]
        }

        ( project\core\playlists\controller\playlist_state.py ) : {   
            PlaylistState [class]
        }

        ( project\core\services\controller\grid_state.py ) : {   
            GridState [class],
            GridMode [class]
        }


## Fluxo de Execução:

    Realização de um loop for em uma lista de strings (os.listdir da pasta de músicas) ou na lista de objetos (SongMetadata).

        ↓
    
    Validação:
        Se a música possuir algum metadado registrado pelo player:
            ↪ Fase 0 (lê os metadados e salva em songs.json)
        Senão:
            ↪ Fase 1 (
                1. Extrai os metadados existentes no arquivo;
                2. Filtragem com base nos dados retornados da extração de metadata;
                3. Classificação das músicas com base na existência de seus metadado;
            )
        
        ↓

    Salva os dados já obtidos e Execução de callbacks.

        ↓
    
    Fase 2 (tratamento de músicas com metadados).

        ↓

    Fase 3 (tratamento de músicas sem metadados, apenas como o nome integral do arquivo .mp3).

        ↓

    Execução de callbacks.
