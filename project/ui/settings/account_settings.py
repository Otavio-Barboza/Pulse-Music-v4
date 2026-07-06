import flet as ft
from project.ui.others.colors import colors
from Assets.App.Services.Controllers.estado_app import EstadoApp
from Assets.App.Services.Auth.google_login_auth import login_google
from Assets.App.Services.gerenciador_contas import GerenciadorContas
from ...App.Usuario.Models.usuario import Usuario

class AccountSettings(ft.Container):
    def __init__(self, page):
        super().__init__(
            alignment = ft.alignment.center,
        )
        self.page = page
        self.data = None

        self.caixa_texto = ft.TextField(
            hint_text = 'Digite novo nome...',
            hint_style = ft.TextStyle(
                color = colors.cinza1,
                size = 16
            ),

            border_radius = ft.border_radius.all(12),
            height = 50,
            filled = True,
            fill_color = colors.preto4,
            border_color = ft.Colors.TRANSPARENT,
            width = 700,
            
            label_style = ft.TextStyle(
                color = colors.branco
            ),
            
            text_style = ft.TextStyle(
                color = colors.branco,
                size = 16
            ),

            cursor_color = colors.amarelo,
            content_padding = ft.Padding(16, 10, 16, 10),
            on_submit = self._novo_nome_user
        )

        self.nome_user = self._retornar_textos(
            texto = '',
            size = 22,
            weight = ft.FontWeight.W_700
        )
        self.email = self._retornar_textos(
            texto = '',
            size = 16,
            weight = ft.FontWeight.W_500
        )
        self.imagem = ft.CircleAvatar(
            foreground_image_src = '',
            radius = 35,
            bgcolor = ft.Colors.TRANSPARENT
        )

        EstadoApp.registrar_ouvinte('conta_atual', self._quando_conta_atualizar)

        usuario = GerenciadorContas.usuario()
        if usuario is not None:
            usuario.registrar_callback(self._atualizar_campos)
            self._atualizar_campos(usuario)
        
        self.selecao_contas = ft.Column(
            visible = False,
            controls = []
        )
        self._criar_selecoes()

        self.content = ft.Container(
            alignment = ft.alignment.center,
            width = 700,

            content = ft.Column(
                alignment = ft.MainAxisAlignment.START,
                horizontal_alignment = ft.CrossAxisAlignment.START,
                spacing = 10,
            
                controls = [
                    ft.Container(
                        bgcolor = colors.preto8,
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
                                    content = self.imagem
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
                                            self.nome_user,
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

                        content = self._retornar_textos(
                            texto = 'Alterar nome de usuário',
                            size = 22,
                            weight = ft.FontWeight.W_500
                        )
                    ),
                    self.caixa_texto,
                    
                    self._criar_botoes(
                        texto_botao = 'Adicionar nova conta', 
                        id = 'nova', 
                        colors_fundo = colors.amarelo3,
                        colors_texto = colors.preto7,
                        funcao = self._acao_itens
                    ),

                    self._criar_botoes(
                        texto_botao = 'Trocar de conta', 
                        id = 'trocar', 
                        colors_fundo = colors.amarelo3,
                        colors_texto = colors.preto7,
                        funcao = self._acao_itens
                    ),
                    self.selecao_contas,
                    
                    self._criar_botoes(
                        texto_botao = 'Excluir atual conta', 
                        id = 'excluir',
                        colors_fundo = colors.preto_puro_3,
                        colors_texto = colors.branco,
                        funcao = self._acao_itens
                    )
                ]
            )
        )
    
    # conteudos
    def retornar_contas_disponiveis(self):
        """
            Função para retornar as contas disponíveis para a seleção de contas.

        Returns:
            list : lista das contas disponíveis.
        """
        conta = GerenciadorContas.contas_cache
        return conta['contas']
    
    # widgets
    def _criar_botoes(self, texto_botao : str, id : str, colors_fundo : str, colors_texto : str | ft.Colors, funcao):
        """
            Função para retornar os botões das principais funcionalides da aba das cofnigurações da conta.

        Args:
            texto_botao (str): texto do botão a ser atribuído
            id (str): sessão responsável pelo botão
            colors_fundo (str): colors do fundo do botão
            colors_texto (str | ft.Colors): colors do texto do botão
            funcao (function | def): função a ser atribuída ao clicar no botão

        Returns:
            ft.TextButton : Botão de texto com as características repassadas na função.
        """
        return ft.TextButton(
            text = texto_botao,
            data = {'acao' : id},
            on_click = funcao,
            width = 250,
            
            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : colors_fundo
                },
                color = {
                    ft.ControlState.DEFAULT : colors.branco,
                    ft.ControlState.HOVERED : colors_texto
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(width = 2, color = colors.branco)
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
    
    def _criar_selecoes(self):
        """
            Função para criar os botões da seleção de contas.
              →  Se houver mais de uma conta dísponivel: Cria a seleção de botões.
              →  Senão: cria um ft.Text informando que não há outras contas a selecionar. 
        """
        lista = self.retornar_contas_disponiveis()
        id_atual = GerenciadorContas.ler_conta_atual_index()
        
        self.selecao_contas.controls.clear()

        if len(lista) == 1:
            self.selecao_contas.controls.append(
                ft.Container(
                    margin = ft.margin.only(left = 30, top = 0, bottom = 0),

                    content = ft.Text(
                        value = 'Não há outras contas salvas. Crie outra para selecioná-la!',
                        weight = ft.FontWeight.W_500,
                        size = 16,
                        color = colors.branco,
                        max_lines = 2,
                        overflow = ft.TextOverflow.FADE
                    )
                )
            )
        else:
            for conta in lista:
                if conta.get('id') != id_atual:
                    self.selecao_contas.controls.append(
                        ft.Container(
                            margin = ft.margin.only(left = 30, top = 0, bottom = 0),
                            
                            content = ft.TextButton(
                                data = {'acao' : 'selecionar', 'id' : conta.get('id')},
                                text = conta.get('nome'),
                                on_click = self._acao_itens,
                                width = 300,

                                style = ft.ButtonStyle(
                                    bgcolor = {
                                        ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                                        ft.ControlState.HOVERED : colors.preto8
                                    },
                                    color = colors.branco,
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

        self.update()

    def _retornar_textos(self, texto : str, size : int, weight : ft.FontWeight):
        """
            Função para retornar os textos da tela de configurações da conta.

        Args:
            texto (str): texto a ser colocado.
            size (int): tamanho do texto.
            weight (ft.FontWeight): expessura do texto.

        Returns:
            ft.Text : texto destinado.
        """
        return ft.Text(
            value = texto,
            style = ft.TextStyle(
                size = size,
                weight = weight,
                overflow = ft.TextOverflow.FADE,
            )
        )
    
    # funçionalidades
    def _novo_nome_user(self, e):
        """
            Função para atualizar o nome do usuário atual pela caixa de texto.

        Args:
            e (evento): evento disparado da submissão do nome inserido no ft.TextField.
        """
        novo_nome = self.caixa_texto.value

        self.nome_user.value = novo_nome
        self.caixa_texto.value = ''
        self.update()

        GerenciadorContas.usuario().nome = novo_nome
        GerenciadorContas.usuario().salvar()
        GerenciadorContas.atualizar_nome_no_index(id_conta = self.data, novo_nome = novo_nome)

    def _atualizar_campos(self, usuario : Usuario):
        """
            Função para atualizar os campos principais chamada em self._quando_conta_atualizar.

        Args:
            usuario (class Usuario): atributos de Usuario.
        """
        self.nome_user.value = usuario.nome
        self.email.value = usuario.email
        self.imagem.foreground_image_src = usuario.imagem
        self.data = usuario.id
        self.update()

    def _quando_conta_atualizar(self, dados : Usuario | dict):
        """
            Callback do EstadoApp: 'dados' será o objeto Usuario (quando carregado) ou o index (quando index foi atualizado). Verificamos o tipo.
        """
        # se vier um objeto Usuario, atualiza direto
        if isinstance(dados, Usuario):
            usuario = dados
            # registra callback para atualizações futuras
            usuario.registrar_callback(self._atualizar_campos)
            self._atualizar_campos(usuario)
            return

        # se vier o index (dict), podemos carregar campos a partir dele:
        if isinstance(dados, dict):
            # tenta pegar id atual do index e buscar usuário em memória
            try:
                id_atual = dados.get("conta_atual")
                if id_atual:
                    # tentar selecionar conta (isso chamará carregar_conta() e notificar novamente)
                    GerenciadorContas.selecionar_conta_por_id(id_atual)
            except Exception:
                pass

        self._criar_selecoes()

    def _trocar_conta_obrigatoria(self, id_nova_conta : str):
        """
            Função para realizar a troca obrigatória da conta ao excluir a atual.
        Args:
            id_nova_conta (str): ID da nova conta selecionada para carregar.
        """
        id_a_ser_excluido = GerenciadorContas.ler_conta_atual_index()

        GerenciadorContas.excluir_conta(id_a_ser_excluido)
        GerenciadorContas.selecionar_conta_por_id(id_nova_conta)
        
    def excluir_conta_atual(self):
        """
            Função para excluir a atual conta.
              →  Se o as contas disponíveis forem mais de que 2: Abre overlay na classe SelecionarContaObrigatoria para a seleção de outra conta.
              →  Senão: Chama diretamente o GerenciadorContas para a exclusão, caso haja uma única disponível, é alterado automáticamente para essa; senão é notificado o EstadoApp ('sem_conta') para realizar o novo login.
        """
        contas = GerenciadorContas.contas_cache['contas']

        if len(contas) > 2:
            self.page.overlay.clear()
            self.page.overlay.append(
                SelecionarContaObrigatória(
                    page = self.page,
                    on_selecionar = self._trocar_conta_obrigatoria
                )
            )
            self.page.update()
        else:
            GerenciadorContas.excluir_conta(self.data)
        
    async def _toggle_trocar_conta(self):
        self.selecao_contas.visible = not self.selecao_contas.visible
        self.update()

    async def _acao_itens(self, e):
        if e.control.data.get('acao') == 'nova':
            await login_google()
            self._criar_selecoes()
        elif e.control.data.get('acao') == 'trocar':
            await self._toggle_trocar_conta()
        elif e.control.data.get('acao') == 'selecionar':
            id_conta = e.control.data['id']
            GerenciadorContas.selecionar_conta_por_id(id_conta)
            self._criar_selecoes()
        elif e.control.data.get('acao') == 'excluir':
            self.excluir_conta_atual()
            self._criar_selecoes()
        else:
            print(e.control.data)

class SelecionarContaObrigatória(ft.Container):
    def __init__(self, page, on_selecionar):
        super().__init__(
            expand = True,
            alignment = ft.alignment.center,
            blur = 5,
            bgcolor = ft.Colors.with_opacity(0.9, colors.preto1)
        )

        self.page = page
        self.on_selecionar = on_selecionar
        self.contas = GerenciadorContas.contas_cache
        self.id_atual = GerenciadorContas.ler_conta_atual_index()
        self.opcoes = ft.Column(controls = [])

        self.content = ft.Container(
            alignment = ft.alignment.center,
            bgcolor = colors.preto7,
            height = 600,
            width = 400,
            padding = ft.padding.all(25),
            border_radius = ft.border_radius.all(15),

            content =  ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER, 
                spacing = 20,
                controls = [
                    ft.Text(
                        value = 'Selecione uma das contas disponíveis.',
                        size = 24,
                        color = colors.branco,
                        weight = ft.FontWeight.BOLD,
                        max_lines = 2,
                        text_align = ft.TextAlign.CENTER
                    ),
                    ft.Divider(),
                    self._retornar_opcoes()
                ]
            )
        )
        
        self.on_click = self.fechar_overlay

    def _selecionar(self, id_conta : str):
        """
            Função que atua como callback para aplicar a abertura e funcionamento da seleção da conta obrigatória.

        Args:
            id_conta (str): ID da conta
        """
        self.on_selecionar(id_conta)
    
    def ao_clicar(self, e):
        """
            Função para 'chamar' o callback self._selecionar

        Args:
            e (evento): evento do clique.
        """
        self._selecionar(e.control.data)
        self.page.overlay.clear()
        self.page.update()
    
    def fechar_overlay(self, e):
        self.page.overlay.clear()
        self.page.update()
    
    def _retornar_opcoes(self):
        """
            Função para retornar a seleção das contas obrigatórias.

        Returns:
            ft.Column : Coluna com os botões.
        """
        return ft.Column(
            ft.TextButton(
                text = conta.get('nome'),
                data = conta.get('id'),
                width = 300,
                on_click = self.ao_clicar,

                style = ft.ButtonStyle(
                    bgcolor = {
                        ft.ControlState.DEFAULT : colors.preto8,
                        ft.ControlState.HOVERED : colors.amarelo3
                    },
                    alignment = ft.alignment.center,
                    color = colors.branco,
                    padding = ft.padding.symmetric(
                        vertical = 15,
                        horizontal = 15
                    ),
                    text_style = ft.TextStyle(
                        size = 16
                    ),
                    shape = ft.RoundedRectangleBorder(radius = 5)
                )
            ) for conta in self.contas['contas'] if conta.get('id') != self.id_atual
        )