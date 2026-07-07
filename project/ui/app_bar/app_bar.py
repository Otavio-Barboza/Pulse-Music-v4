from project.ui.others.colors import color
from Assets.App.Meta.Controller.scanner_controller import ScannerController
import flet as ft

class AppBar(ft.AppBar):
    def __init__(self, abrir_config):
        super().__init__(
            bgcolor = color.preto7,
            leading_width = 50,

            title = ft.Container(
                on_click = self.fechar_overlays,
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    
                    controls = [
                        ft.CircleAvatar(
                            radius = 20,
                            bgcolor = color.branco,
        
                            content = ft.Image(
                                src = r'Assets/Global/Images/Logo/logo_v2.png',
                                border_radius = 100
                            )
                        ),
                        ft.Text(
                            value = 'Pulse Music',
                            font_family = 'sansita',
                            size = 38,
                            text_align = ft.TextAlign.LEFT
                        )
                    ]
                )
            )
        )

        self.abrir_config = abrir_config
        
        self.config_btn = ft.IconButton(
            icon = ft.Icons.SETTINGS,
            on_click =  lambda e: self.abrir_config()
        )
        
        self.icon_status = ft.Container(
            content = ft.Icon(
                name = ft.Icons.SYNC_ROUNDED
            ),
            on_click = self.mostrar_conteudo_icon_status
        )
        
        self.texto_drawer = self._retornar_texto(
            texto = 'Scanner desativado'
        )
        
        self.conteudo_drawer = ft.NavigationDrawer(
            open = False,
            bgcolor = ft.Colors.TRANSPARENT,
            
            controls = [
                ft.Container(
                    height = 400,
                    alignment = ft.alignment.center,
                    bgcolor = color.preto2,
                    margin = ft.margin.all(20),
                    padding = ft.padding.only(
                        bottom = 10,
                        top = 10,
                        left = 20,
                        right = 20    
                    ),
                    border_radius = ft.border_radius.only(
                        top_left = 10,
                        bottom_left = 10,
                        bottom_right = 10
                    ),
                    content = self.texto_drawer
                )
            ]
        )
        
        self.actions = [
            self.icon_status,
            self.config_btn
        ]
        
        self.page.end_drawer = self.conteudo_drawer

        ScannerController.registar_callback(
            evento = 'informacao_processo_scanner',
            funcao = self.alterar_texto_drawer
        )
        ScannerController.registar_callback(
            evento = 'icone_status_scanner',
            funcao = self.alterar_icone
        )
        ScannerController.registar_callback(
            evento = 'progress_status_scanner',
            funcao = self.alterar_progress
        )

    def fechar_overlays(self, e):
        self.page.overlay.clear()
        self.page.update()
        
    def mostrar_conteudo_icon_status(self, e):
        self.page.open(self.conteudo_drawer)
        self.page.update()
        
    def _retornar_texto(self, texto : str) -> ft.Text:
        return ft.Text(
            value = texto,
            text_align = ft.TextAlign.LEFT,
            size = 14.5,
            weight = 500
        )
    
    def alterar_texto_drawer(self, texto : str):
        self.texto_drawer.value = texto
        self.page.update()

    def alterar_icone(self, dados = None):
        self.icon_status.content = ft.ProgressRing(
            scale = 0.5,
            color = color.amarelo
        )
        self.icon_status.update()

    def alterar_progress(self, dados = None):
        self.icon_status.content = ft.Icon(
            name = ft.Icons.SYNC_ROUNDED
        )
        self.icon_status.update()