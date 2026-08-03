# Estrutrura do songs.json


## Qual objetivo desse arquivo?

- Este arquivo é responsável por armazenar a base de dados necessários (nesse caso excluí-se favoritas e letras);
- Também é o arquivo principal usado como cache e auxiliar para os outros arquivos .json e outros caches específicos. 


## Qual utilidade dos dados salvos?

- A utilidade desses dados tratam-se para a exibição geral como: 
    - Abas de artistas e álbuns; 
    - Nome de artistas na listagem de músicas e no player de reprodução; 
    - Reprodução específica por artista ou álbum.


## Dependências Diretas:

    Enum:

        ( project\core\meta\enum\status.py ) : {
            SongStatus [class : enum]
        } 


## Estrutura:

    {
        "song_path" : Path( 
            Caminho da pasta em que o arquivo se localiza 
        ),
        
        "playlist_id" : str( 
            ID da playlist cujo song_path a pertence 
        ),
        
        "artist_id" : str( 
            Identificador único criado para cada artista, referenciado depois no artists.json como auxilio na identificação mais próxima do correto.
        ),

        "mp3_file" : str( 
            Nome integral do arquivo .mp3 
        ),

        "mp3_file_filtered" : dict[str or None, str or None] {
            "title" : str( 
                Titulo integral do arquivo .mp3 filtrado 
            ),

            "artist" : str( 
                Artista do arquivo .mp3 filtrado 
            ),
        },
        
        "id3_data" : dict[str, dict[str, str or None]] {
            "original_data" : {
                "title" : str( 
                    Titulo ID3 extraído, ainda original 
                ),

                "artist_id3" : str( 
                    Artista ID3 nativo no arquivo 
                )
            },

            "filtered_data" : {
                "title" : str( 
                    Titulo ID3 filtrado 
                ),

                "artist" : str( 
                    Artista obtido pela filtragem do titulo ID3 
                )
            }
        },
        
        "defined_artist" : str( 
            Artista final, definitivo na decisão;
            Se nenhum identificado, considera-se como desconhecido
        ),

        "artist_metadata " : dict[str, str or Path or None] = {
            "id_deezer" : str( 
                ID retornado pela API da Deezer
            ),
          
            "medium" : str(
                Imagem de tamanho medium retornada pela API da Deezer do respectivo artista; 
                
                A imagem é salva fisicamente no diretório: (
                    Seu Diretório\APPDATA\LOCAL\Barboza Software\Pulse Music\account\sua conta logada\images\artists
                )    
            ),
          
            "big" : {
                "link" : str(
                    Imagem de tamanho big retornada pela API da Deezer do respectivo artista;
                    A imagem é referenciada pelo link retornado pela Deezer. 
                ),
            
                "path" : str(
                    Caminho do arquivo da respectiva música do artista atribuído;

                    Esse parâmetro referência a imagem big que é imbutida como um novo metadado no arquivo .mp3, por isso o caminho do arquivo é salvo aqui;

                    Essa imagem big, é lida em base64 quando é clicado na imagem do artista exibido na aba 'artistas', assim abrindo a tela expandida com imagem big.
                )
            } 
        },

        "album_metadata" : dict[str, str | Path] = {
            "id_deezer" : str( 
                ID retornado pela API da Deezer 
            ),

            "name" : str( 
                Nome do álbum obtido 
            ),

            "medium" : str(
                Imagem de tamanho medium retornada pela API da Deezer do respectivo álbum; 
                
                A imagem é salva fisicamente no diretório: (
                    Seu Diretório\APPDATA\LOCAL\Barboza Software\Pulse Music\account\sua conta logada\images\albums
                )    
            ),
          
            "big" : {
                "link" : str(
                    Imagem de tamanho big retornada pela API da Deezer do respectivo álbum;
                    A imagem é referenciada pelo link retornado pela Deezer. 
                ),
             
                "path" : str(
                    Caminho do arquivo da respectiva música do álbum atribuído;

                    Esse parâmetro referência a imagem big que é imbutida como um novo metadado no arquivo .mp3, por isso o caminho do arquivo é salvo aqui;

                    Essa imagem big, é lida em base64 quando é clicado na imagem do álbum exibido na aba 'artistas', assim abrindo a tela expandida com imagem big.
                )
            } 
        },


        <!-- métricas de validação de artistas para os casos de músicas que contenham apenas o seu titulo musical de informação -->
        
        "metrics" : {
            "score" : int or float, defaut = 0 ( 
                score obtido da similaridade 
            ),
           
            "status" : SongStatus [class] ( 
                Status final da música 
            ),
           
            "gap" : float or None, defaut = None ( 
                Valor das métricas de validação usadas para decidir o artista final 
            ),
           
            "consensus" : float or None, defaut = None ( 
                Valor das métricas de validação usadas para decidir o artista final 
            ),
          
            "sim_1" : float or None, defaut = None ( 
                Valor das métricas de validação usadas para decidir o artista final 
            ),
           
            "sim_2" : float or None, defaut = None ( 
                Valor das métricas de validação usadas para decidir o artista final 
            )
        }
    }
