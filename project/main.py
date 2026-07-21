# imports de arquivos de interface
from ui.app_bar.app_bar import AppBar
from ui.player_section.section_player import PlayerSection
from ui.settings.screen_settings import ScreenSettings
from ui.navigation.tabs import TabsNavigation
from ui.others.colors import color
from ui.others.overlay_login import OverlayLogin

# imports de arquivos back-end
from core.utils.utils import Utils
from core.utils.path import AppPaths
from core.services.account_manager import AccountManager
from core.services.controllers.resize_manager import ResizeManager
from core.song.model.audio import AudioLoop
from core.song.controller.reproduction_manager import ReproductionManager
from core.meta.models.scanner_model import ScannerModel
from core.meta.cache.global_cache import cache_metadata
from core.meta.cache.cache_artists import CacheArtists
from core.lyrics.cache.cache_lyrics import CacheLyrics

# imports de bibliotecas  gerais
from pathlib import Path
import asyncio
import flet as ft


"""
    _summary_: ordem de execução do main()
        ├── Configurar Page
        │
        ├── Declarar funções auxiliares
        │
        ├── Validar login
        │
        ├── Carregar cache
        │
        ├── Criar componentes principais
        │
        ├── Componentes.load()
        │
        ├── page.add(...)
        │
        ├── Registrar callbacks globais e componentes.connect()
        │
        ├── Inicializações finais
        │
        └── Disparar eventos globais
"""


def open_profile(current_id: str) -> dict:
    """
        Função para abrir o perfil.json e retornar os dados do perfil da atualc conta logada.

    Args:
        current_id (str) : ID da conta logada atualmente.

    Returns:
        dict : Dicionário contendo as informações do perfil da conta logada
    """
    return Utils.sync_load_json(AppPaths.ACCOUNT / current_id / "profile.json")
   

async def main(page: ft.Page):

    """  Configurações da page, gerais da aplicação  """

    page.title = "Pulse Music"
    page.padding = 0
    page.bgcolor = color.preto_puro_4
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "sansita" : r"assets\fonts\SansitaSwashed.ttf",
        "google_sans_flex" : r"assets\fonts\GoogleSansFlex.ttf"
    }
    page.theme = ft.Theme(
        font_family = "google_sans_flex"
    )
    

    """  Declarar funções auxiliares  """

    # configurações do app
    def open_configurations():
        """
            Função para abrir as configurações em overlay.
        """     
        
        page.overlay.append(ScreenSettings(page))
        page.update()

    # carregamento de cache
    async def load_cache():
        data: dict = await Utils.sync_load_json(f"Assets/Data/Contas/{AccountManager.contas_cache['conta_atual']}/Music/musicas.json")
        cache_metadata.load(data)
        
        await CacheArtists.load()
        CacheLyrics.load_cache()

    # função para validar o login
    async def validate_login() -> bool:
        """
            Função que valida o login. 
              →  Retorna True se houver alguma conta logada. 
              →  Retorna False de nenhuma conta existir/estiver logada.
        """

        current_id = AccountManager.read_current_account_index()

        if current_id is None:
            return False
        
        data = AccountManager.search_account_index(current_id)
        profile = open_profile(current_id)

        AccountManager.load_account(
            account_id = current_id,
            base_path = Path(data["base_path"]),   
            data = profile
        )

        return True
        
    # overlay do primeiro login
    async def abrir_overlay():
        _overlay = OverlayLogin(page)

        page.overlay.append(_overlay)
        page.update()

        await _overlay.login_finished.wait()

        _overlay.opacity = 0
        _overlay.update()

        await asyncio.sleep(1)

        page.overlay.remove(_overlay)
        page.update()
    
    
    """  Validar login  """

    if not await validate_login():
        # carrega uma overlay dinâmivo para o usuário fazer o login via google, quando terminar acontece uma animação fade out e carrega o restante de todo o app.
        await abrir_overlay()


    """  Carregar cache  """

    # await load_cache()
    

    """  Criar componentes principais  """

    page.appbar = AppBar(
        open_configurations = open_configurations, 
        page = page
    )
    tabs = TabsNavigation(page)
    player = PlayerSection(page)

    
    """  Carregando componentes  """

    tabs.load()
    player.load()


    """  Adicionando componentes a page  """
    
    page.add(
        ft.SafeArea(
            expand = True,

            content = ft.Stack(
                expand = True,
                
                controls = [
                    ft.Column(
                        expand = True,
                        spacing = 0,

                        controls = [
                            tabs,
                            player.compact
                        ]
                    ),

                    player.expanded
                ]
            )
        )
    )


    """  Registrando callbacks dos componentes  """

    # callbacks individuais dos componentes
    
    tabs.connect()
    player.connect()


    """  Inicializações gerais  """

    tabs.playlist.load()
    tabs.pesquisa_musica.start_animation()
    tabs.load_favorites()
    
    page.on_resized = ResizeManager.to_execute
   
    # AudioLoop.start()
    # ReproductionManager.start()


    """  Notificação e execução de eventos globais  """
    
    # page.run_task(
    #     ScannerModel.async_start_scanner
    # )


if __name__ == "__main__":
    asyncio.run(
        ft.app_async(
            target = main, 
            assets_dir = "assets"
        )
    )