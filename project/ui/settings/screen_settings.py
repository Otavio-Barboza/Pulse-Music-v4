from project.ui.others.colors import colors
from project.ui.settings.account_settings import AccountSettings
from project.ui.settings.about_settings import AboutSettings
from project.ui.settings.settings_support import SettingsSupport
from project.ui.settings.other_settings import OtherSettings
from Assets.App.Services.Controllers.estado_app import EstadoApp
import flet as ft

class ScreenSettings(ft.Container):
    def __init__(self, page):
        super().__init__(
            expand = True,
            bgcolor = colors.preto6,
            padding = 0
        )
        self.page = page

        # dicionário que guarda todos os botões
        self.botoes = {}

        # registrar para escutar mudanças de seção
        EstadoApp.registrar_ouvinte('secao_config', self._quando_secao_mudar)
        
        self.menu_lateral = self._menu_lateral()

        self.area_conteudo = ft.Container(
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
                self.menu_lateral,
                self.area_conteudo
            ]
        )

    def _menu_lateral(self):
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
                        value = 'Configurações', 
                        size = 26, 
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    ),
                    ft.Divider(),

                    self._criar_botao(texto = 'Conta', id_secao = 'conta'),
                    self._criar_botao(texto = 'Sobre o Player', id_secao = 'sobre'),
                    self._criar_botao(texto = 'Aparência', id_secao = 'aparencia'),
                    self._criar_botao(texto = 'Outras Configurações', id_secao = 'outros'),
                    self._criar_botao(texto = 'Suporte', id_secao = 'suporte'),

                    ft.Divider(),
                    ft.TextButton(
                        text = 'Fechar',
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

    def _criar_botao(self, texto : str, id_secao : str):
        """
            Cria os botões do menú lateral das configurações e depois armazena eles no dict self.botoes

        Args:
            texto (str): Texto que irá compor o nome do botão
            id_secao (str): Seção a qual será destinada ao botão

        Returns:
            ft.TextButton: Botoão de texto
        """

        botao = ft.TextButton(
            text = texto,
            width = 200,
            on_click = lambda e: self._selecionar(id_secao),
        
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

        self.botoes[id_secao] = botao
        return botao

    def _selecionar(self, id_secao : str):
        """
            Quando é clicado em algum botão a ação é registrada no ouvinte do EstadoApp com o id_secao 

        Args:
            id_secao (str): Seção responsável de conteúdo
        """
        EstadoApp.selecionar_secao_config(id_secao)

    def _quando_secao_mudar(self, id_secao : str):
        """
            1. Altera o Conteúdo da seção principal conforme o botão clicado
            2. Navega nos intens do dict de botões para atualizar a colors, isso caso a seção da chave seja a mesma que o id_secao informado

        Args:
            id_secao (str): Seção responsável
        """

        conteudo_atual = self.area_conteudo.content
        if hasattr(conteudo_atual, 'parar_loop'):
            conteudo_atual.parar_loop()
        if id_secao == 'conta':
            self.area_conteudo.content = AccountSettings(page = self.page)
        elif id_secao == 'sobre':
            sobre = AboutSettings(page = self.page)
            self.area_conteudo.content = sobre
            sobre.iniciar_loop()
        elif id_secao == 'aparencia':
            self.area_conteudo.content = ft.Column(
                expand = True,
                controls = [
                    ft.Text('Em Desenvolvimento Configurações de Aparência', size=18)
                ]
            )
        elif id_secao == 'outros':
            self.area_conteudo.content = OtherSettings(page = self.page)
        elif id_secao == 'suporte':
            self.area_conteudo.content = SettingsSupport(page = self.page)

        self.area_conteudo.update()

        for chave, botao in self.botoes.items():
            if chave == id_secao:
                # botão selecionado → colors diferente
                botao.style.bgcolor = {
                    ft.ControlState.DEFAULT: colors.amarelo3,
                    ft.ControlState.HOVERED: colors.amarelo,
                }
                botao.style.color = colors.preto1
            else:
                botao.style.bgcolor = {
                    ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED: colors.preto4,
                }
                botao.style.color = colors.branco

            botao.update()