# OPERAÇÃO DO PIPELINE: ARQUIVOS, RESPONSABILIDADES E DEPEDÊNCIAS.


## Arquivos:

    pipeline.md:
        - Fluxo geral do pipeline;
        - Orquestrador das execuções do inicio ao fim.


    phase_1.md:
        - Classificação inicial dos metadados.


    phase_2.md:
        - Resolução utilizando ID3 e Deezer.


    phase_3.md:
        - Resolução baseada no filename (nome integral do arquivo .mp3).


## Dependências:

    Repositório (repository):

        ( project\core\meta\repository\filtering ) : {
            Filtering
        }

        ( project\core\meta\repository\extract_metadata ) : {
            ExtractMetadata
        }

        ( project\core\meta\repository\metadata_repository.py ) : {
            MetadataRepository
        }


    Cache:

        ( project\core\meta\cache\cache_artists.py ) : {
            CacheArtists
        } 


    Modelo (model):
        ( project\core\meta\models\song.py ) : {
            SongMetadata
        }


## Responsabilidades:

1. **Reposítório:**
    - Responsável pelas tarefas e execuções de persistência como gerenciamento de arquivos, tarefas diversas, utilitários e etc.

2. **Model(s):**
    - Modelos de objetos ou classes bases de operação.

3. **Cache**
    - Cache ou memória interna e temporária do app para melhor fluxo e flexibilidade na operação do aplicativo.