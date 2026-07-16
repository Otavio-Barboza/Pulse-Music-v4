# imports de arquivos de interface
from ui.app_bar.app_bar import AppBar
from ui.player_section.section_player import PlayerSection
from ui.settings.screen_settings import ScreenSettings
from ui.navigation.tabs import TabsNavigation
from ui.others.colors import color

# imports de arquivos back-end
from core.services.controllers.state_app import StateApp
from core.services.auth.google_login_auth import login_google
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
            Função para abrir as configurações em overlay (repassada por parâmetro no AppBar em "open_configurations").
        """     
        
        page.overlay.append(ScreenSettings(page))
        page.update()


    # gerenciamento de contas
    async def on_sem_conta(_ = None):
        """
            Função chamada quando é notficado pelo StateApp estar ("no_account") existente, consequentemente chama o login_google() para realizá-lo.
        """
        page.overlay.clear()
        page.update()
        await login_google()
        StateApp.notify("current_account", None)
    
    async def validate_login():
        """
            Função que valida o login. 
              →  Se tiver conta logada: notifica o StateApp ("conta_atual") para realizar o carregamento do usuario e informações ao player. 
              →  Senão: notifica o StateApp ("no_account") para realizar o login pelas contas Google.
        """

        current_id = AccountManager.read_current_account_index()

        if current_id is not None:
            data = AccountManager.search_account_index(current_id)
            profile = open_profile(current_id)

            AccountManager.load_account(
                account_id = current_id,
                base_path = Path(data["base_path"]),   
                data = profile
            )
        else:
            StateApp.notify("no_account")

    # def on_current_account(*_):
    #     """
    #         Função para carregar o conteúdo principal do app quando uma conta estiver logada.

    #     Args:
    #         usuario (class Usuario) : O usuário atual é repassado a função tornando mainupulável diretamente ao conteúdo do main.
    #     """
    #     nonlocal tabs
    #     tabs.playlist.carregar()

    # carregamento de cache
    async def load_cache():
        data: dict = await Utils.sync_load_json(f"Assets/Data/Contas/{AccountManager.contas_cache['conta_atual']}/Music/musicas.json")
        cache_metadata.load(data)
        
        await CacheArtists.load()
        CacheLyrics.load_cache()


    """  Validar login  """

    await validate_login()


    """  Carregar cache  """

    # await load_cache()
    

    """  Criar componentes principais  """

    page.appbar = AppBar(open_configurations = open_configurations, page = page)
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
                            player.compacto
                        ]
                    ),

                    player.expandido
                ]
            )
        )
    )


    """  Registrando callbacks dos componentes e globais  """

    # callbacks globais 
    StateApp.register_callback("no_account", on_sem_conta)
    StateApp.register_callback("current_account", tabs.playlist.carregar)

    # callbacks individuais dos componentes
    tabs.connect()
    player.connect()


    """  Inicializações gerais  """

    tabs.pesquisa_musica.iniciar_animacao()
    tabs.carregar_favoritas()
    
    page.on_resized = ResizeManager.to_execute
   
    # AudioLoop.start()
    # ReproductionManager.start()


    """  Notificação e execução de eventos globais  """
    
    page.run_task(
        ScannerModel.async_start_scanner
    )

    # StateApp.notify(
    #     "current_account",
    #     AccountManager.user()
    # )


if __name__ == "__main__":
    asyncio.run(
        ft.app_async(
            target = main, 
            assets_dir = "assets"
        )
    )