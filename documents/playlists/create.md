# Aruivos, Dependências e Fluxo de Execução: CREATE.


**Arquivos:**
-

    [ front-end ] ( project\ui\playlist\ ) : {
        overlay.py,
        overlay_tip.py (overlay dicas),
        content_playlist.py (orquestrador e container base do conteúdo),

        base\
            base_playlists.py (base exibida com buttons + content_playlist),
            grid_playlists.py (grid dos cards de playlist),
            
        containers\
            container_card.py
    }

    [ back-end ] ( project\core\playlist\ ) : {
        controller\
            playlist_manager.py,
            playlist_state.py

        enum\
            playlist_enum.py

        models\
            playlist_card.py
            playlist_config.py
            platlist.py

        repository\
            path.py
            playlist_repository.py
    }


**Dependências:**
-

    ( project\ui\playlist\ ) : {
        overlay.py,
        overlay_tip.py (overlay dicas),
        content_playlist.py (orquestrador e container base do conteúdo),

        base\
            base_playlists.py (base exibida com buttons + content_playlist),
            grid_playlists.py (grid dos cards de playlist),
            
        containers\
            container_card.py
    }

**Fluxo de Execução:**
-