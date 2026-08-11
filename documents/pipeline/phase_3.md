# ESTRUTURA DA FASE 3


## Objetivos:

Resolver o restante das músicas com base no seu nome integral filtrado.


## Arquivos:

    ( project\core\meta\pipeline ) : {
        phase_3.py
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

    
    Modelo (models):
    
        ( project\core\meta\models\song.py ) : {
            SongMetadata [class]
        } 


    Enum:
    
        ( project\core\meta\enum\status.py ) : {
            SongStatus [class : enum]
        } 


    Provedor (provider):

        ( project\core\meta\provider\deezer.py ) : {
            FontManager [class]
        } 
    

    Cache:

        ( project\core\meta\cache\cache_artists.py ) : {
            CacheArtists [class]
        } 

    
    Pipeline:

        ( project\core\meta\pipeline\helpers\analysis.py ) : {
            analyze_consensus [function] (
                itens: lista de tracks provenientes da deezer
            ),

            choose_artist [function] (
                score: float,
                best_item: dict,
                song: SongMetadata
            ),

            calculate_phase3_score_with_artist [function] (
                filter: dict,
                item: dict
            ),

            calculate_score_title_only_phase_3 [function] (
                filter: dict,
                item: dict
            ),

            sort_artists_by_title_only [function] (
                gap: float,
                sim_1: float,
                top5: list[ dict[ str, str ] ]
            )
        } 


    Services:

        ( project\core\services\account_manager.py ) : {
            AccountManager [class]
        } 


    Utils:

        ( project\core\utils\path.py ) : {
            AppPaths [class]
        } 


## Fluxo de Execução:

    Filtra os dados com base no nome integral do arquivo .mp3.

        ↓

    Se a filtragem for mal sucedida:
        ↪ Defini-se alguns dados previamente como não existentes (None/null).

        ↓

    Faz busca pela música na API da Deezer.
    
        ↓
    
    Se houver artista no nome do arquivo:
        ↪ Retorna os nomes.
    Senão:
        ↪ tenta obter algum artista com base em score, senão for relevante define como desconhecido.

        ↓
        
    Valida os dados retornados pela condição anterior (se none o retorno, defini-se com valores nulos os dados).

        ↓

    Se existir apenas o titulo:
        ↪ Baixa e registra dos dados (imagens, json, metadados) com base no dado de artista existente.
    Senão:
        ↪ Baixa e registra dos dados (imagens, json, metadados).
