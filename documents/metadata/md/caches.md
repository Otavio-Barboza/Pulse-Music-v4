# Estrutrura do artists.json e cache_metadata


## Qual objetivo do artists.json?

- Este arquivo é responsável por armazenar a base de artistas existentes baseando-se em songs.json;


## Qual utilidade dos dados salvos (artists.json)?

- Também é usado como validador de artistas, ele mantém uma precisão maior na definição final dos artistas com suporte a aliases suportando o mesmo artistas de maneiras diferentes em sua gravação em um formatdo de ID (uuid) por artista. Desta forma cada artista é referenciado pelo seu ID, padronizando o que aparece ou não. 


## Dependências Diretas:

    Repositório (repository):

        ( project\core\meta\repository\metadata_repository.py ) : {
            MetadataRepository [class]
        },

        ( project\core\meta\repository\filtering.py ) : {
            Filtering [class]
        } 


## Arquivos Base e Operação:

    Cache:

        ( project\core\meta\cache ) : {
            cache_artists.py : {
                descrições : (
                    --> Classe usada para referenciar como o Cache de artistas;
                    --> Auxilia e gerencia o artists.json;
                    --> Manipulação e organização dos IDs de artistas e aliases por similaridade [SequenceMatcher].
                ),

                componente principal : (
                    CacheArtists [class]
                )
            },

            cache_data.py : {
                descrições : (
                    --> Gerenciador base de caches (álbuns, artistas e traks [songs.json]); 
                    --> Faz a intermediação do gerenciamento e carregamento dos caches (artistas e álbuns). 
                ),

                componente principal : (
                    CacheMetadata
                )
            },

            global_cache.py : (
                Referencia a classe CacheMetadata na variável global de uso: cache_metadata : CacheMetadata
            )
        }


## Estrutura:

### CacheArtists:

- Essa classe é exclusiva no cache temporário de gerenciamento de artistas pelo pipeline ao artists.json

### CacheMetadata:

- Essa classe é a gerenciadora dos caches:

    ### self.tracks [dict]:
    - Refere-se ao songs.json;
    
    ### Artist [class] (self.artists [dict]):
    - Cache responável pela relação entre artistas e músicas suas;
    - Usa como base self.tracks em suas chaves (artist_id e defined_artist);
    - Com base nisso, cada artist_id torna-se uma chave no dict do cache, com nome e músicas em aliases do mesmo artista (song_key (chave da música)).

    ### Album [class] (self.albums [dict]):
    - Cache responável pela relação entre álbuns e músicas suas;
    - Usa como base self.tracks em suas chaves (name do álbum e song_key (chave da música));
    - Com base nisso, cada name torna-se uma chave no dict do cache, com a chave das músicas e seus caminhos em aliases do mesmo álbum.