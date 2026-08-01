# import de interface
from ui.others.colors import color

# import de back-end
from core.meta.controller.scanner_controller import ScannerController
from core.utils.path import AppPaths

# imports geral
import flet as ft


class AppBar(ft.AppBar):
    def __init__(self, open_configurations, page: ft.Page):
        super().__init__(
            bgcolor = color.preto7,
            leading_width = 50,

            title = ft.Container(
                on_click = self.close_overlay,
                content = ft.Row(
                    alignment = ft.MainAxisAlignment.START,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    
                    controls = [
                        ft.CircleAvatar(
                            radius = 20,
                            bgcolor = color.branco,
        
                            content = ft.Image(
                                src = r"assets\images\logos\logo_v2.png",
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
        self.page = page
        self.open_configurations = open_configurations
        
        self.config_btn = ft.IconButton(
            icon = ft.Icons.SETTINGS,
            on_click =  lambda e: self.open_configurations(),
            data = "config"
        )
        
        self.icon_status = ft.Container(
            data = "status",
            content = ft.Icon(
                name = ft.Icons.SYNC_ROUNDED
            ),
            on_click = self.open_content_icon_status
        )

        self.connection_button = ft.IconButton(
            icon = ft.Icons.WIFI_OFF_OUTLINED,
            data = "connection",
            on_click = self.open_information_connection
        )
        
        self.drawer_text = self._create_text(
            text = 'Scanner desativado'
        )
        
        self.drawer_content = ft.NavigationDrawer(
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
                    content = self.drawer_text
                )
            ]
        )
        
        self.actions = [
            self.icon_status,
            self.config_btn
        ]

        self.page.end_drawer = self.drawer_content

        ScannerController.register_callback(
            event = 'processes_information_scanner',
            function = self.alter_text_drawer
        )
        ScannerController.register_callback(
            event = 'icon_status_scanner',
            function = self.alter_icon
        )
        ScannerController.register_callback(
            event = 'progress_status_scanner',
            function = self.alter_progress
        )

    def close_overlay(self, e):
        self.page.overlay.clear()
        self.page.update()
        
    def open_content_icon_status(self, e):
        self.page.open(self.drawer_content)
        self.page.update()
        
    def _create_text(self, text : str) -> ft.Text:
        return ft.Text(
            value = text,
            text_align = ft.TextAlign.LEFT,
            size = 14.5,
            weight = 500
        )
    
    def alter_text_drawer(self, text : str):
        self.drawer_text.value = text
        self.page.update()

    def alter_icon(self, *_):
        self.icon_status.content = ft.ProgressRing(
            scale = 0.5,
            color = color.amarelo
        )
        self.icon_status.update()

    def alter_progress(self, *_):
        self.icon_status.content = ft.Icon(
            name = ft.Icons.SYNC_ROUNDED
        )
        self.icon_status.update()

    def open_information_connection(self, event):
        self.page.open(
            ft.NavigationDrawer(
                bgcolor = ft.Colors.TRANSPARENT,
                position = ft.NavigationDrawerPosition.END,

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

                        content = ft.Column(
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            alignment = ft.MainAxisAlignment.CENTER,
                            spacing = 15,

                            controls=[
                                ft.Icon(
                                    ft.Icons.WIFI_OFF_ROUNDED,
                                    size = 50,
                                    color = ft.Colors.ORANGE,
                                ),

                                ft.Text(
                                    "Sem conexão com a internet",
                                    size = 20,
                                    weight = ft.FontWeight.BOLD,
                                    text_align = ft.TextAlign.CENTER,
                                ),

                                ft.Text(
                                    "Alguns recursos online, como letras, downloads e sincronização, "
                                    "podem não estar disponíveis no momento.\n\n"
                                    "Verifique sua conexão para restaurar o acesso.",
                                    size = 14,
                                    text_align = ft.TextAlign.CENTER,
                                )
                            ]
                        )
                    )
                ]
            )
        )