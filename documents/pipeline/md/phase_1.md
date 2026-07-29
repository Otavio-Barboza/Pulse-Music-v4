# ESTRUTURA DA FASE 1


## Objetivos:

Classificar as músicas com base em seus metadados.


## Arquivos:

    ( project\core\meta\pipeline ) : {
        phase_1.py
    } 


## Dependências Diretas:

    Repositório (repository):

        ( project\core\meta\repository\tasks.py ) : {
            Task [class]
        } 

        ( project\core\meta\repository\extract_metadata.py ) : {
            ExtractMetadata [class]
        } 


    Modelo (Model):

        ( project\core\meta\models\song.py ) : {
            SongMetadata [class]
        } 


    Enum:

        ( project\core\meta\enum\status.py ) : {
            SongStatus [class : enum]
        } 


## Fluxo de Execução:

    Calcula o score do artista id3 (metadado nativo) com o artista da filtragem (titulo id3).

        ↓

    Se o score for maior ou igual a 0.85:
        ↪ Organiza os dados com status de AMBOS (artistas extremamente confiáveis).
    Caso se o score for maior ou igual a 0.65 e menor que 0.85:
        ↪ Organiza os dados com status de MEDIUM (artistas meramente confiáveis).
    Senão:
        ↪ Organiza os dados com status de INCONSISTENT (artistas divergentes).
