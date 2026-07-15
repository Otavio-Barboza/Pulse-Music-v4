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

    # configurações gerais do app
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
    
    
    # variaveis globais do app
    settings: ScreenSettings | None = None

    
    # funções auxiliares
    async def on_sem_conta(_ = None):
        """
            Função chamada quando é notficado pelo StateApp estar ("no_account") existente, consequentemente chama o login_google() para realizá-lo.
        """
        page.overlay.clear()
        page.update()
        await login_google()
    
    StateApp.register_callback("no_account", on_sem_conta)
    
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

    async def load_cache():
        data: dict = await Utils.sync_load_json(f"Assets/Data/Contas/{AccountManager.contas_cache['conta_atual']}/Music/musicas.json")
        cache_metadata.load(data)
        
        await CacheArtists.load()
        CacheLyrics.load_cache()

    def open_configurations():
        """
            Função para abrir as configurações em overlay (repassada por parâmetro no AppBar em "open_configurations").
        """     

        if settings is None:
            settings = ScreenSettings()
            page.overlay.append(settings)
        else:
            if settings not in page.overlay:
                page.overlay.append(settings)
        page.update()

    await validate_login()
    # await load_cache()

    tabs = TabsNavigation()

    async def on_current_account(usuario):
        """
            Função para carregar o conteúdo principal do app quando uma conta estiver logada.

        Args:
            usuario (class Usuario) : O usuário atual é repassado a função tornando mainupulável diretamente ao conteúdo do main.
        """
        tabs.playlist.carregar()
    
    StateApp.register_callback("current_account", on_current_account)
    
    player = PlayerSection()
    page.appbar = AppBar(open_configurations = open_configurations)
    
    page.add(
        ft.SafeArea(
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
    
    StateApp.notify(
        "current_account",
        AccountManager.user()
    )

    tabs.pesquisa_musica.iniciar_animacao()
    tabs.carregar_favoritas()
    
    page.on_resized = ResizeManager.to_execute
   
    AudioLoop.start()
    ReproductionManager.start()
     
    page.run_task(
        ScannerModel.async_start_scanner
    )


if __name__ == "__main__":
    asyncio.run(
        ft.app_async(
            target = main, 
            assets_dir = "assets"
        )
    )