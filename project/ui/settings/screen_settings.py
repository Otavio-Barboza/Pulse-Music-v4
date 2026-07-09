# imports de interface
from project.ui.others.colors import colors
from project.ui.settings.account_settings import AccountSettings
from project.ui.settings.about_settings import AboutSettings
from project.ui.settings.settings_support import SettingsSupport
from project.ui.settings.other_settings import OtherSettings

# imports de back-end
from project.core.services.controllers.state_app import StateApp

# import geral
import flet as ft


class ScreenSettings(ft.Container):
    def __init__(self):
        super().__init__(
            expand = True,
            bgcolor = colors.preto6,
            padding = 0
        )

        # dicionário que guarda todos os botões
        self.buttons = {}

        # registrar para escutar mudanças de seção
        StateApp.register_callback("configurations_session", self._quando_secao_mudar)
        
        self.side_menu = self._side_menu()

        self.content_area = ft.Container(
            expand = True,
            padding = 20,
            bgcolor = colors.preto2,
            border_radius = ft.border_radius.only(
                top_left = 10,
                bottom_left = 10
            ),

            content = AccountSettings(page = self.page)
        )

        self.content = ft.Row(
            spacing = 5,
            controls = [
                self.side_menu,
                self.content_area
            ]
        )

    def _side_menu(self):
        """
            Cria o menú lateral das configurações

        Returns:
            ft.Container: Menú lateral das configurações
        """

        return ft.Container(
            width = 250,
            bgcolor = colors.preto7,
            padding = ft.padding.all(20),
            border_radius = ft.border_radius.only(
                top_right = 10, 
                bottom_right = 10
            ),

            content = ft.Column(
                controls = [
                    ft.Text(
                        value = "Configurações", 
                        size = 26, 
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    ),
                    ft.Divider(),

                    self._create_button(text = "Conta", section_id = "account"),
                    self._create_button(text = "Sobre o Player", section_id = "about"),
                    self._create_button(text = "Aparência", section_id = "appearance"),
                    self._create_button(text = "Outras Configurações", section_id = "others"),
                    self._create_button(text = "Suporte", section_id = "support"),

                    ft.Divider(),

                    ft.TextButton(
                        text = "Fechar",
                        width = 200,
                        icon = ft.Icons.CLOSE_ROUNDED,

                        style = ft.ButtonStyle(
                            bgcolor = {
                                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                                ft.ControlState.HOVERED : colors.amarelo4
                            },
                            text_style = ft.TextStyle(
                                size = 16,
                                weight = ft.FontWeight.BOLD
                            ),
                            padding = ft.padding.symmetric(
                                vertical = 20,
                                horizontal = 15
                            ),
                            color = {
                                ft.ft.ControlState.DEFAULT : colors.branco,
                                ft.ft.ControlState.HOVERED : colors.preto_puro
                            },
                            alignment = ft.alignment.center,
                            icon_size = 20
                        ),
                        on_click = lambda e: self.page.overlay.remove(self) or self.page.update()
                    )
                ]
            )
        )

    def _create_button(self, text : str, section_id : str):
        """
            Cria os botões do menú lateral das configurações e depois armazena eles no dict self.buttons

        Args:
            text (str): Texto que irá compor o nome do botão
            section_id (str): Seção a qual será destinada ao botão

        Returns:
            ft.TextButton: Botoão de text
        """

        botao = ft.TextButton(
            text = text,
            width = 200,
            on_click = lambda e: self._selecionar(section_id),
        
            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : colors.preto4
                },
                padding = ft.padding.symmetric(
                    vertical = 20,
                    horizontal = 10
                ),
                text_style = ft.TextStyle(
                    size = 16,
                    weight = ft.FontWeight.W_500
                ),

                color = colors.branco,
                shape = ft.RoundedRectangleBorder(radius = 5),
                alignment = ft.alignment.center_left
            )
        )

        self.buttons[section_id] = botao
        return botao

    def _selecionar(self, section: str):
        """
            Quando é clicado em algum botão a ação é registrada no ouvinte do StateApp com o section 

        Args:
            section (str): Seção responsável de conteúdo
        """
        StateApp.select_config_section(section)

    def _quando_secao_mudar(self, section_id: str):
        """
            1. Altera o Conteúdo da seção principal conforme o botão clicado
            2. Navega nos intens do dict de botões para atualizar a colors, isso caso a seção da chave seja a mesma que o section_id informado

        Args:
            section_id (str): Seção responsável
        """

        current_content = self.content_area.content

        if hasattr(current_content, "parar_loop"):
            current_content.parar_loop()
        if section_id == "account":
            self.content_area.content = AccountSettings(page = self.page)
        elif section_id == "about":
            about = AboutSettings(page = self.page)
            self.content_area.content = about
            about.iniciar_loop()
        elif section_id == "appearance":
            self.content_area.content = ft.Column(
                expand = True,
                controls = [
                    ft.Text("Em Desenvolvimento Configurações de Aparência", size=18)
                ]
            )
        elif section_id == "others":
            self.content_area.content = OtherSettings(page = self.page)
        elif section_id == "support":
            self.content_area.content = SettingsSupport(page = self.page)

        self.content_area.update()
        
        key: str
        button: ft.Icons
        
        for key, button in self.buttons.items():
            if key == section_id:
                # botão selecionado → colors diferente
                button.style.bgcolor = {
                    ft.ControlState.DEFAULT: colors.amarelo3,
                    ft.ControlState.HOVERED: colors.amarelo,
                }
                button.style.color = colors.preto1
            else:
                button.style.bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED: colors.preto4,
                }
                button.style.color = colors.branco

            button.update()