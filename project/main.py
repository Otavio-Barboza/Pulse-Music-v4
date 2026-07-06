from project.ui.app_bar.app_bar import AppBar
from project.ui.player_section.section_player import PlayerSection
from project.ui.settings.screen_settings import ScreenSettings
from project.ui.navigation.tabs import TabsNavigation
from project.ui.others.colors import color
from Assets.App.Audio.Model.audio import AudioLoop
from Assets.App.Audio.Controller.sessao import SessaoReproducao
from Assets.App.Services.Controllers.estado_app import EstadoApp
from Assets.App.Services.Controllers.estado_redimensionamento import ResizeManager
from Assets.App.Services.Auth.google_login_auth import login_google
from Assets.App.Services.gerenciador_contas import GerenciadorContas
from Assets.App.Meta.Repository.persistencia import Persistencia
from Assets.App.Meta.Models.scanner_model import ScannerModel
from Assets.App.Meta.Memoria.memoria_global import memoria
import asyncio, json
import flet as ft

def abrir_perfil(id_atual):
    """
        Função para abrir o perfil.json e retornar os dados do perfil da atualc conta logada.

    Args:
        id_atual (str) : ID da conta logada atualmente.

    Returns:
        dict : Dicionário contendo as informações do perfil da conta logada
    """
    with open(f"Assets/Data/Contas/{id_atual}/perfil.json") as js:
        dados_perfil = json.load(js)
        return dados_perfil
   
async def main(page : ft.Page):
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
    
    config_painel = None


    async def on_sem_conta(_ = None):
        """
            Função chamada quando é notficado pelo EstadoApp estar ("sem_conta") existente, consequentemente chama o login_google() para realizá-lo.
        """
        page.overlay.clear()
        page.update()
        await login_google()
    
    EstadoApp.registrar_ouvinte("sem_conta", on_sem_conta)
    
    async def validar_login():
        """
            Função que valida o login. 
              →  Se tiver conta logada: notifica o EstadoApp ("conta_atual") para realizar o carregamento do usuario e informações ao player. 
              →  Senão: notifica o EstadoApp ("sem_conta") para realizar o login pelas contas Google.
        """
        id_atual = GerenciadorContas.ler_conta_atual_index()

        if id_atual is not None:
            dados = GerenciadorContas._buscar_conta_index(id_atual)
            perfil = abrir_perfil(id_atual)

            GerenciadorContas.carregar_conta(
                id_conta = id_atual,
                pasta_base = dados["pasta_base"],   
                dados = perfil
            )
        else:
            EstadoApp.notificar("sem_conta")

    async def carregar_memoria():
        from Assets.App.Meta.Memoria.memoria_global import memoria
        from Assets.App.Meta.Memoria.memoria_artistas import MemoriaArtistas
        from Assets.App.Letras.Cache.memoria_letras import LetrasMemoria

        dados = await Persistencia.ler_json(f"Assets/Data/Contas/{GerenciadorContas.contas_cache['conta_atual']}/Music/musicas.json")
        memoria.carregar(dados)
        
        await MemoriaArtistas.carregar()
        LetrasMemoria.carregar_memoria()

    def abrir_config():
        """
            Função para abrir as configurações em overlay (repassada por parâmetro no AppBar em "abrir_config").
        """
        nonlocal config_painel
         
        if config_painel is None:
            config_painel = ScreenSettings(page)
            page.overlay.append(config_painel)
        else:
            if config_painel not in page.overlay:
                page.overlay.append(config_painel)
        page.update()

    await validar_login()
    await carregar_memoria()

    tabs = TabsNavigation(page = page)

    async def on_conta_atual(usuario):
        """
            Função para carregar o conteúdo principal do app quando uma conta estiver logada.

        Args:
            usuario (class Usuario) : O usuário atual é repassado a função tornando mainupulável diretamente ao conteúdo do main.
        """
        tabs.playlist.carregar()
    
    EstadoApp.registrar_ouvinte("conta_atual", on_conta_atual)
    
    player = PlayerSection(page = page)
    page.appbar = AppBar(page = page, abrir_config = abrir_config)
    
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
    
    EstadoApp.notificar(
        "conta_atual",
        GerenciadorContas.usuario()
    )

    tabs.pesquisa_musica.iniciar_animacao()
    tabs.carregar_favoritas()
    
    page.on_resized = ResizeManager.executar
   
    AudioLoop.iniciar()
    SessaoReproducao.inicar()
     
    page.run_task(
        ScannerModel._async_iniciar_scanner
    )


if __name__ == "__main__":
    asyncio.run(
        ft.app_async(
            target = main, 
            assets_dir = "assets"
        )
    )