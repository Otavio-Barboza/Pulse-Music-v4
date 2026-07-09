# import de interface
from project.ui.others.colors import color

# imports de back-end
from project.core.playlists.enum.playlist_enum import PlalistOverlayMode
from ...App.Meta.Pipeline.pipeline import Pipeline

# imports gerais
from tkinter import filedialog, Tk
import flet as ft
import asyncio


class ContainerOverlay(ft.Container):
    def __init__(self, estado, conteudo, modo : PlalistOverlayMode):
        super().__init__(
            alignment = ft.alignment.center,
            expand = True
        )

        self.conteudo = conteudo
        self.estado = estado
        self.modo = modo

        self.albuns, self.capas, self.caminhos = self.estado._retornar_imagens()
        self.cards = []
        self.cores = []

        self.container_cor_opacidade = ft.Container(
            col = 4,
            height = 150,
            width = 100,
            border_radius = ft.border_radius.all(20),
            bgcolor = ft.Colors.BLACK12
        )

        self.slider_opacidade = ft.Slider(
            on_change = self._change_slider,
            value = 1.0,
            max = 1.0,
            min = 0,
            thumb_color = color.amarelo,
            active_color = color.amarelo,
            inactive_color = color.preto2,
            overlay_color = color.amarelo_opaco2
        )

        self.texto_pasta = ft.Text(
            col = 6,
            value = 'Nenhuma pasta de musicas selecionada',
            size = 16,
            max_lines = 1,
            text_align = ft.TextAlign.CENTER
        )

        self.texto_nome = ft.Text(
            col = 6,
            value = 'Adicione o nome da sua playlist',
            size = 18,
            max_lines = 2,
            text_align = ft.TextAlign.CENTER
        )

        self.caixa_texto = ft.TextField(
            hint_text = 'Digite o nome da sua playlist...',
            hint_style = ft.TextStyle(
                color = color.cinza1,
                size = 16
            ),

            border_radius = ft.border_radius.all(12),
            max_length = 500,
            min_lines = 1,
            max_lines = 1,
            multiline = False,
            filled = True,
            fill_color = color.preto4,
            border_color = ft.Colors.TRANSPARENT,
            col = 8,
            
            label_style = ft.TextStyle(
                color = color.branco
            ),
            
            text_style = ft.TextStyle(
                color = color.branco,
                size = 16
            ),

            cursor_color = color.amarelo,
            content_padding = ft.Padding(16, 10, 16, 10),

            on_submit = self._submeter_nome,
            on_change = self._chage
        )

        self.content = ft.Container(
            alignment = ft.alignment.center,
            bgcolor = color.preto8,
            width = 900,
            height = 900,
            border_radius = ft.border_radius.all(20),
            padding = ft.padding.all(10),

            content = ft.Column(
                spacing = 10,
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.ResponsiveRow(
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.CENTER,
                        height = 80,

                        controls = [
                            self.caixa_texto,
                            
                            self._criar_botoes(click = 'pasta', texto = 'Selecionar Pasta com as Músicas', col = 4, on_cor_fundo = color.laranja2, cor_texto = color.branco)    
                        ]
                    ),

                    ft.ResponsiveRow(
                        alignment = ft.MainAxisAlignment.CENTER,
                        controls = [
                            self.texto_nome,
                            self.texto_pasta
                        ]
                    ),

                    ft.Divider(),

                    ft.Container(
                        height = 680,

                        content = ft.Tabs(
                            selected_index = 0,
                            animation_duration = 300,
                            label_color = color.amarelo,
                            divider_color = ft.Colors.TRANSPARENT,
                            indicator_color = ft.Colors.TRANSPARENT,
                            overlay_color = color.preto8,
                            unselected_label_color = color.branco_puro,
                            scrollable = False,
                            expand = True,
                            tab_alignment = ft.TabAlignment.FILL,
                            
                            label_text_style = ft.TextStyle(
                                size = 16,
                                weight = ft.FontWeight.BOLD,
                                letter_spacing = 1,
                                font_family = 'sansita'
                            ),

                            unselected_label_text_style = ft.TextStyle(
                                weight = ft.FontWeight.W_300
                            ),

                            tabs = [
                                ft.Tab(
                                    text = 'Albuns',
                                    content = ft.GridView(
                                        max_extent = 220,
                                        controls = [
                                            self._criar_cards_img(f'{self.caminhos[0]}/{img}') for img in self.albuns
                                        ]
                                    )
                                ),

                                ft.Tab(
                                    text = 'Capas de Músicas',

                                    content = ft.GridView(
                                        max_extent = 220,

                                        controls = [
                                            self._criar_cards_img(f'{self.caminhos[1]}/{img}') for img in self.capas
                                        ]
                                    )
                                ),

                                ft.Tab(
                                    text = 'Cor de Fundo da Playlist',

                                    content = ft.Container(
                                        padding = ft.padding.only(top = 10),

                                        content = ft.Column(
                                            controls = [
                                                ft.Container(
                                                    height = 200,
                                                    content = ft.ResponsiveRow(
                                                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                                        controls = [
                                                            self.container_cor_opacidade,

                                                            ft.Column(
                                                                alignment = ft.MainAxisAlignment.CENTER,
                                                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                                                col = 8,

                                                                controls = [
                                                                    ft.Text(
                                                                        value = 'Regule a opacidade da color',
                                                                        size = 16,
                                                                        text_align = ft.TextAlign.CENTER
                                                                    ),

                                                                    self.slider_opacidade,
                                                                    
                                                                    self._criar_botoes(
                                                                        click = 'opacidade',
                                                                        col = None,
                                                                        texto = 'Salvar Opacidade',
                                                                        on_cor_fundo = color.azul_medio2,
                                                                        cor_texto = color.branco
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ),

                                                ft.Divider(),

                                                ft.Container(
                                                    expand = True,

                                                    content = ft.GridView(
                                                        max_extent = 150,

                                                        controls = [
                                                            self._criar_cards_cores(color) for color in color._paleta_de_cores()
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    )
                                )
                            ]
                        )
                    ),

                    ft.ResponsiveRow(
                        controls = [
                            self._criar_botoes(
                                click = 'cancelar', 
                                texto = 'Cancelar', 
                                col = 6,
                                on_cor_fundo = color.vermelho,
                                cor_texto = color.branco
                            ),

                            self._criar_botoes(
                                click = 'concluir', 
                                texto = 'Concluir', 
                                col = 6,
                                on_cor_fundo = color.amarelo,
                                cor_texto = color.preto1
                            )
                        ]
                    )
                ]
            )
        )

        if self.modo == PlalistOverlayMode.UPDATE:
            self._preencher_campos()

    def _preencher_campos(self):
        playlist = self.estado.playlist_config  # PlaylistDetalhada

        self.estado.nome = playlist.nome
        self.estado.color = playlist.style["color"]
        self.estado.opacidade = playlist.style["opacidade"]
        self.estado.imagem = playlist.style["pasta"]
        self.estado.pasta = playlist.musicas["pasta"]

        self.container_cor_opacidade.bgcolor = playlist.style["color"]
        self.container_cor_opacidade.opacity = playlist.style["opacidade"]
        self.texto_nome.value = f"Nome da playlist: {playlist.nome}"
        self.texto_pasta.value = f"Pasta: {playlist.musicas['pasta']}"

    def _criar_cards_img(self, imagem):
        card = ft.Container(
            height = 220,
            width = 220,
            data = imagem,
            alignment = ft.alignment.top_right,
            on_click = self._selecionar_imagem,
            image = ft.DecorationImage(
                src = imagem,
                fit = ft.ImageFit.COVER
            ),
            padding = ft.padding.all(5),
            border_radius = ft.border_radius.all(5),
            
            content = ft.Icon(
                name = ft.Icons.CHECK,
                color = color.amarelo,
                size = 30,
                visible = False
            )
        )

        self.cards.append(card)
        return card
    
    def _criar_cards_cores(self, color : ft.Colors):
        cont = ft.Container(
            width = 100,
            height = 100,
            border_radius = ft.border_radius.all(100),
            bgcolor = color,
            alignment = ft.alignment.center,
            data = color,
            on_click = self._selecionar_cor,

            content = ft.Text(
                value = color.replace('Colors.', '').upper(),
                text_align = ft.TextAlign.CENTER,
                weight = ft.FontWeight.W_300
            )
        )

        self.cores.append(cont)
        return cont
    
    def _confirmar(self, e):
        if self.modo == PlalistOverlayMode.CREATE:
            self.criar_play()
        elif self.modo == PlalistOverlayMode.UPDATE:
            self.estado.atualizar_playlist()
            self._fechar_overlay(e=None)


    def _criar_botoes(self, click, col : int, texto : str, cor_texto : str, on_cor_fundo : str) -> ft.TextButton:
        if click == 'cancelar':
            click = self._fechar_overlay
        elif click == 'concluir':
            click = self._confirmar
        elif click == 'pasta':
            click = self._abrir_seletor_pasta
        elif click == 'opacidade':
            click = self._salvar_opacidade
        else:
            click =  None
        
        return ft.TextButton(
            col = col,
            text = texto,
            on_click = click,
            height = 40,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : on_cor_fundo
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2, color.branco)
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : cor_texto
                },
                padding = ft.padding.all(10)
            )
        )
    
    def _selecionar_imagem(self, e):
        self.estado.imagem = e.control.data

        for card in self.cards:
            if card.data == e.control.data:
                card.opacity = 0.9
                card.scale = 1.1
                card.content.visible = True
            else:
                card.opacity = 1.0
                card.scale = 1.0
                card.content.visible = False
            
            card.update()
    
    def _change_slider(self, e):
        self.container_cor_opacidade.opacity = self.slider_opacidade.value
        self.container_cor_opacidade.update()

    def _selecionar_cor(self, e):
        self.estado.color = e.control.data
        self.container_cor_opacidade.bgcolor = e.control.data
        self.container_cor_opacidade.update()
        
        for container in self.cores:
            color = container.content.value

            if container.data == e.control.data:
                container.scale = 1.1
                container.content.weight = ft.FontWeight.BOLD
            else:
                container.scale = 1.0
                container.content.weight = ft.FontWeight.W_300
            
            container.update()

    def _salvar_opacidade(self, e):
        cor_opc = ft.Colors.with_opacity(
            color = self.estado.color, 
            opacity = self.container_cor_opacidade.opacity
        )

        self.estado.color = cor_opc
        self.estado.opacidade = self.container_cor_opacidade.opacity

        self.page.open(
            ft.SnackBar(
                content = ft.Text('Valor de Opacidade Salva')
            )
        )

    def _submeter_nome(self, e):
        self.estado.nome = self.caixa_texto.value
        self.texto_nome.value = f'Nome da playlist: {self.caixa_texto.value}'
        self.caixa_texto.value = ''
        self.update()
    
    def _chage(self, e):
        self.estado.nome = self.caixa_texto.value
        self.texto_nome.value = f'Nome da playlist: {self.caixa_texto.value}'
        self.update()

    def _abrir_seletor_pasta(self, e):
        root = Tk()
        root.withdraw()
        pasta = filedialog.askdirectory()
        root.destroy()
        

        if pasta in self.verificar_caminhos_existentes():
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Já existe uma playlist com essa pasta de músicas, escolha outra!')
                )
            )
            self.page.update()
        else:
            self.estado.pasta = pasta
            self.texto_pasta.value = f'Pasta selecionada: {pasta}'
            self.texto_pasta.update()
    
    def _fechar_overlay(self, e):
        self.estado.imagem = r'Assets\Global\Images\Padrao\capa_playlist_padrao.png'
        self.estado.nome = None
        self.estado.color = '#3d3d3d'
        self.estado.opacidade = 1.0
        self.estado.pasta = None
        
        self.page.overlay.clear()
        self.page.update()

    async def rodar_pipeline(self, pasta : str, id : str):
        await asyncio.to_thread(
            Pipeline._processar_wrapper_sync,
            pasta,
            [],
            id
        )

    def verificar_playlists_existentes(self) -> list[str]:
        return self.estado.retornar_playlists_existentes()

    def verificar_caminhos_existentes(self) -> list[str]:
        return self.estado.retornar_pastas_existentes()

    def criar_play(self):
        if self.estado.nome is None:
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Atribua um nome a sua playlist primeiro')
                )
            )
            self.page.update()
        elif self.estado.nome in self.verificar_playlists_existentes():
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Já existe uma playlist com esse nome, escolha outro!')
                )
            )
            self.page.update()
        elif self.estado.pasta is None:
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Selecione uma pasta para criar')
                )
            )
            self.page.update()
        elif self.estado.pasta in self.verificar_caminhos_existentes():
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Já existe uma playlist com essa pasta de músicas, escolha outra!')
                )
            )
            self.page.update()
        else:
            id = self.estado.criar_playlist()
            self.page.run_task(
                self.rodar_pipeline,
                self.estado.pasta,
                id
            )
            self._fechar_overlay(e = None)