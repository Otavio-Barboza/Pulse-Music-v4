# import de interface
from ui.others.colors import color

# imports de back-end
from core.services.controllers.state_app import StateApp
from core.services.auth.google_login_auth import login_google
from core.services.account_manager import AccountManager
from core.user.models.user import User

# import geral
import flet as ft


class AccountSettings(ft.Container):
    def __init__(self, page):
        super().__init__(
            alignment = ft.alignment.center,
        )
        self.page = page
        self.data = None

        self.text_field = ft.TextField(
            hint_text = 'Digite novo nome...',
            hint_style = ft.TextStyle(
                color = color.cinza1,
                size = 16
            ),

            border_radius = ft.border_radius.all(12),
            height = 50,
            filled = True,
            fill_color = color.preto4,
            border_color = ft.Colors.TRANSPARENT,
            width = 700,
            
            label_style = ft.TextStyle(
                color = color.branco
            ),
            
            text_style = ft.TextStyle(
                color = color.branco,
                size = 16
            ),

            cursor_color = color.amarelo,
            content_padding = ft.Padding(16, 10, 16, 10),
            on_submit = self.new_user_name
        )

        self.user_name = self._create_text(
            text = '',
            size = 22,
            weight = ft.FontWeight.W_700
        )
        self.email = self._create_text(
            text = '',
            size = 16,
            weight = ft.FontWeight.W_500
        )
        self.image_account = ft.CircleAvatar(
            foreground_image_src = '',
            radius = 35,
            bgcolor = ft.Colors.TRANSPARENT
        )

        # StateApp.register_callback('current_account', self.update_fields)
        
        if AccountManager.user() is not None:
            # user.register_callback(self.update_fields)
            self.update_fields()
        
        self.account_selection = ft.Column(
            visible = False,
            controls = []
        )
        self._create_selections()

        self.content = ft.Container(
            alignment = ft.alignment.center,
            width = 700,

            content = ft.Column(
                alignment = ft.MainAxisAlignment.START,
                horizontal_alignment = ft.CrossAxisAlignment.START,
                spacing = 10,
            
                controls = [
                    ft.Container(
                        bgcolor = color.preto8,
                        border_radius = ft.border_radius.all(10),
                        alignment = ft.alignment.center,
                        padding = ft.padding.symmetric(
                            vertical = 15,
                            horizontal = 5
                        ),

                        content = ft.ResponsiveRow(
                            col = 12,
                            vertical_alignment = ft.CrossAxisAlignment.CENTER,

                            controls = [
                                ft.Container(
                                    col = {'xs' : 12, 'md' : 3},
                                    alignment = ft.alignment.center,
                                    content = self.image_account
                                ),
                                
                                ft.Container(
                                    col = {'xs' : 12, 'md' : 9},
                                    alignment = ft.alignment.center_left,
                                    padding = ft.padding.only(
                                        top = 10,
                                        bottom = 10,
                                        right = 15,
                                        left = 0
                                    ),

                                    content = ft.Column(
                                        horizontal_alignment = ft.CrossAxisAlignment.START,
                                        spacing = 5,                 
                                        controls = [
                                            self.user_name,
                                            self.email
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                    
                    ft.Container(
                        padding = ft.padding.only(
                            left = 0.9,
                            top = 10
                        ),

                        content = self._create_text(
                            text = 'Alterar nome de usuário',
                            size = 22,
                            weight = ft.FontWeight.W_500
                        )
                    ),
                    self.text_field,
                    
                    self._create_button(
                        text_button = 'Adicionar nova conta', 
                        id = 'new', 
                        background_color = color.amarelo3,
                        text_color = color.preto7,
                        function = self._action_items
                    ),

                    self._create_button(
                        text_button = 'Trocar de conta', 
                        id = 'alter', 
                        background_color = color.amarelo3,
                        text_color = color.preto7,
                        function = self._action_items
                    ),
                    self.account_selection,
                    
                    self._create_button(
                        text_button = 'Excluir atual conta', 
                        id = 'delete',
                        background_color = color.preto_puro_3,
                        text_color = color.branco,
                        function = self._action_items
                    )
                ]
            )
        )
    
    # conteudos
    def return_available_accounts(self) -> list[dict]:
        """
            Função para retornar as accounts disponíveis para a seleção de accounts.

        Returns:
            list : lista das accounts disponíveis.
        """
        return AccountManager.accounts_cache.get("accounts")
    
    # widgets
    def _create_button(
        self, 
        text_button: str, 
        id: str, 
        background_color: str, 
        text_color: str | ft.Colors, 
        function
    ):
        """
            Função para retornar os botões das principais funcionalides da aba das cofnigurações da conta.

        Args:
            text_button (str): text do botão a ser atribuído
            id (str): sessão responsável pelo botão
            background_color (str): color do fundo do botão
            text_color (str | ft.Colors): color do text do botão
            function (function | def): função a ser atribuída ao clicar no botão

        Returns:
            ft.TextButton : Botão de text com as características repassadas na função.
        """
    
        return ft.TextButton(
            text = text_button,
            data = {'action' : id},
            on_click = function,
            width = 250,
            
            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : background_color
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : text_color
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(width = 2, color = color.branco)
                },
                padding = ft.padding.symmetric(
                    vertical = 17.5,
                    horizontal = 17.5
                ),
                text_style = ft.TextStyle(
                    size = 18
                ),
                shape = ft.RoundedRectangleBorder(radius = 15),
                alignment = ft.alignment.center_left
            )
        )
    
    def _create_selections(self):
        """
            Função para criar os botões da seleção de accounts.
              →  Se houver mais de uma conta dísponivel: Cria a seleção de botões.
              →  Senão: cria um ft.Text informando que não há outras accounts a select. 
        """
        
        _list_accounts: list[dict] = self.return_available_accounts()
        _current_id: str = AccountManager.read_current_account_index()
        
        # print(_list_accounts)

        self.account_selection.controls.clear()

        if len(_list_accounts) == 1:
            self.account_selection.controls.append(
                ft.Container(
                    margin = ft.margin.only(left = 30, top = 0, bottom = 0),

                    content = ft.Text(
                        value = 'Não há outras accounts salvas. Crie outra para selecioná-la!',
                        weight = ft.FontWeight.W_500,
                        size = 16,
                        color = color.branco,
                        max_lines = 2,
                        overflow = ft.TextOverflow.FADE
                    )
                )
            )
        else:
            account: dict

            for account in _list_accounts:
                if account.get('id') != _current_id:
                    self.account_selection.controls.append(
                        ft.Container(
                            margin = ft.margin.only(left = 30, top = 0, bottom = 0),
                            
                            content = ft.TextButton(
                                data = {'action' : 'select', 'id' : account.get('id')},
                                text = account.get('name'),
                                on_click = self._action_items,
                                width = 300,

                                style = ft.ButtonStyle(
                                    bgcolor = {
                                        ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                                        ft.ControlState.HOVERED : color.preto8
                                    },
                                    color = color.branco,
                                    padding = ft.padding.symmetric(
                                        vertical = 15,
                                        horizontal = 15
                                    ),
                                    text_style = ft.TextStyle(
                                        size = 16
                                    ),
                                    shape = ft.RoundedRectangleBorder(radius = 5),
                                    alignment = ft.alignment.center_left
                                )
                            ) 
                        )
                    )

        # self.update()

    def _create_text(self, text: str, size: int, weight: ft.FontWeight):
        """
            Função para retornar os textos da tela de configurações da conta.

        Args:
            text (str): text a ser colocado.
            size (int): tamanho do text.
            weight (ft.FontWeight): expessura do text.

        Returns:
            ft.Text : text destinado.
        """
        return ft.Text(
            value = text,
            style = ft.TextStyle(
                size = size,
                weight = weight,
                overflow = ft.TextOverflow.FADE,
            )
        )
    
    # funçionalidades
    def new_user_name(self, e):
        """
            Função para atualizar o nome do usuário atual pela caixa de text.

        Args:
            e (evento): evento disparado da submissão do nome inserido no ft.TextField.
        """
        new_name: str = self.text_field.value

        self.user_name.value = new_name
        self.text_field.value = ''
        self.update()

        AccountManager.user().name = new_name
        AccountManager.save_accounts_json()
        AccountManager.save_profile_json()
        AccountManager.update_name_in_index(
            account_id = self.data, 
            new_name = new_name
        )

    def update_fields(self):
        """
            Função para atualizar os campos principais chamada em self.when_account_updates.
        """
        self.user_name.value = AccountManager.user().name
        self.email.value = AccountManager.user().email
        self.image_account.foreground_image_src = AccountManager.user().image
        self.data = AccountManager.user().id
        self.update()

    async def switch_mandatory_account(self, id_new_account: str):
        """
            Função para realizar a troca obrigatória da conta ao delete a atual.
        Args:
            id_nova_conta (str): ID da new conta selecionada para carregar.
        """

        _id_to_delete: str = AccountManager.read_current_account_index()

        await AccountManager.delete_account(
            page = self.page,
            account_id = _id_to_delete
        )
        AccountManager.select_account_by_id(id_new_account)
        
        self._create_selections()
        self.update_fields()
        self.update()
        
    async def delete_current_account(self):
        """
            Função para delete a atual conta.
              →  Se o as account disponíveis forem mais de que 2: Abre overlay na classe SelecionarContaObrigatoria para a seleção de outra conta.
              →  Senão: Chama diretamente o AccountManager para a exclusão, caso haja uma única disponível, é alterado automáticamente para essa; senão é notificado o StateApp ('sem_conta') para realizar o novo login.
        """
        account = AccountManager.accounts_cache['accounts']

        if len(account) > 2:
            self.page.overlay.append(
                SelecionarContaObrigatória(
                    page = self.page,
                    function = self.switch_mandatory_account
                ) 
            )
            self.page.update()
        else:
            await AccountManager.delete_account(
                page = self.page,
                account_id = self.data)

            self._create_selections()
            self.update_fields()
            self.update()
        
    async def _toggle_switch_account(self):
        self.account_selection.visible = not self.account_selection.visible
        self.update()

    async def _action_items(self, e):
        if e.control.data.get('action') == 'new':
            await login_google(self.page)
            
            self.update_fields()
            self._create_selections()
            self.update()
        elif e.control.data.get('action') == 'alter':
            await self._toggle_switch_account()
        elif e.control.data.get('action') == 'select':
            account_id = e.control.data["id"]
            AccountManager.select_account_by_id(account_id)

            self._create_selections()
            self.update_fields()
            self.update()
        elif e.control.data.get('action') == 'delete':
            await self.delete_current_account()
        else:
            print(e.control.data)


class SelecionarContaObrigatória(ft.Container):
    def __init__(self, function: callable, page: ft.Page):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            blur = 5,
            bgcolor = ft.Colors.with_opacity(0.9, color.preto1)
        )   
        self.page = page
        self.function = function

        self.accounts = AccountManager.accounts_cache
        self.current_id = AccountManager.read_current_account_index()
        self.options = ft.Column(controls = [])

        self.content = ft.Container(
            alignment = ft.alignment.center,
            bgcolor = color.preto7,
            height = 600,
            width = 400,
            padding = ft.padding.all(25),
            border_radius = ft.border_radius.all(15),

            content =  ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER, 
                spacing = 20,
                controls = [
                    ft.Text(
                        value = 'Selecione uma das accounts disponíveis.',
                        size = 24,
                        color = color.branco,
                        weight = ft.FontWeight.BOLD,
                        max_lines = 2,
                        text_align = ft.TextAlign.CENTER
                    ),
                    ft.Divider(),
                    self._create_options()
                ]
            )
        )
        
        self.on_click = self.close_overlay
    
    async def _on_click(self, e):
        """
            Função para 'chamar' o callback self._select

        Args:
            e (evento): evento do clique.
        """
        print(f"E.CONTROL.DATA: {e.control.data}")
        await self.function(e.control.data)
        self.page.overlay.remove(self)
        self.page.update()
    
    def close_overlay(self, e):
        self.page.overlay.remove(self)
        self.page.update()
    
    def _create_options(self):
        """
            Função para retornar a seleção das accounts obrigatórias.

        Returns:
            ft.Column : Coluna com os botões.
        """
        return ft.Column(
            ft.TextButton(
                text = account.get('name'),
                data = account.get('id'),
                width = 300,
                on_click = self._on_click,

                style = ft.ButtonStyle(
                    bgcolor = {
                        ft.ControlState.DEFAULT : color.preto8,
                        ft.ControlState.HOVERED : color.amarelo3
                    },
                    alignment = ft.alignment.center,
                    color = color.branco,
                    padding = ft.padding.symmetric(
                        vertical = 15,
                        horizontal = 15
                    ),
                    text_style = ft.TextStyle(
                        size = 16
                    ),
                    shape = ft.RoundedRectangleBorder(radius = 5)
                )
            ) for account in self.accounts['accounts'] if account.get('id') != self.current_id
        )