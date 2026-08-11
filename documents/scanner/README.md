# OPERAÇÃO DO SCANNER: ARQUIVOS, RESPONSABILIDADES E DEPEDÊNCIAS.


**Arquivos:**
-

    Scanner:

        ( project\core\meta\scanner\scanner.py ) : {
            Scanner [class]
        } 

    
    Models:

        ( project\core\meta\models\sacnner_model.py ) : {
            ScannerModel [class]
        } 


**Dependências:**
-

    Meta:

        ( project\core\meta\repository\metadata_repository.py ) : {
            MetadataRepository [class]
        } 

        ( project\core\meta\controller\scanner_controller.py ) : {
            ScannerController [class]
        } 
        
        ( project\core\meta\enum\status.py ) : {
            ScannerStatus [class : enum]
        } 


    Playlists: 

        ( project\core\meta\enum\playlist_enum.py ) : {
            PlaylistLoaded [class : enum]
        } 

        ( project\core\meta\controller\PlaylistState.py ) : {
            PlaylistState [class]
        } 

        ( project\core\meta\repository\path.py ) : {
            CreatePlaylist [class]
        } 
    

    Services:

        ( project\core\services\account_manager.py ) : {
            AccountManager [class]
        } 

        ( project\core\services\controllers\grid_state.py ) : {
            GridState [class],
            GridMode [class : enum]
        } 


**Responsabilidades:**
-

1. **Scanner:**
    - Responsável por executar funções e o fluxo de operação do scanner. As principais funcionalidades estão centralizadas nesta classe.

2. **ScannerModel:**
    - Responsável pela base e ordenamento da execução do scanner em si. Chamado no main para iniciar o loop além de variáveis auxiliares de status da execução.