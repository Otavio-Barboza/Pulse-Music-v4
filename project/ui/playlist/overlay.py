# import de interface
from ui.others.colors import color

# imports de back-end
from core.playlists.enum.playlist_enum import PlalistOverlayMode
from core.meta.pipeline.pipeline import Pipeline

# imports gerais
from tkinter import filedialog, Tk
import flet as ft
import asyncio


class ContainerOverlay(ft.Container):
    def __init__(self, state, mode : PlalistOverlayMode, page: ft.Page):
        super().__init__(
            alignment = ft.alignment.center,
            expand = True
        )   
        self.page = page
        self.state = state # PlaylistManager
        self.mode = mode

        self.albums, self.covers, self.paths = self.state.return_images()
        self.cards = []
        self.colors = []

        self.container_color_opacity = ft.Container(
            col = 4,
            height = 150,
            width = 100,
            border_radius = ft.border_radius.all(20),
            bgcolor = ft.Colors.BLACK12
        )

        self.opacity_slider = ft.Slider(
            on_change = self._change_slider,
            value = 1.0,
            max = 1.0,
            min = 0,
            thumb_color = color.amarelo,
            active_color = color.amarelo,
            inactive_color = color.preto2,
            overlay_color = color.amarelo_opaco2
        )

        self.path_text = ft.Text(
            col = 6,
            value = 'Nenhuma path de musicas selecionada',
            size = 16,
            max_lines = 1,
            text_align = ft.TextAlign.CENTER
        )

        self.text_name = ft.Text(
            col = 6,
            value = 'Adicione o name da sua playlist',
            size = 18,
            max_lines = 2,
            text_align = ft.TextAlign.CENTER
        )

        self.text_field = ft.TextField(
            hint_text = 'Digite o name da sua playlist...',
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

            on_submit = self._submit_name,
            on_change = self._change
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
                            self.text_field,
                            
                            self._create_button(
                                click = 'path', 
                                text = 'Selecionar Pasta com as Músicas', 
                                col = 4, 
                                background_color = color.laranja2, 
                                text_color = color.branco
                            )    
                        ]
                    ),

                    ft.ResponsiveRow(
                        alignment = ft.MainAxisAlignment.CENTER,
                        controls = [
                            self.text_name,
                            self.path_text
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
                                            self._create_image_card(f'{self.paths[0]}/{img}') for img in self.albums
                                        ]
                                    )
                                ),

                                ft.Tab(
                                    text = 'Capas de Músicas',

                                    content = ft.GridView(
                                        max_extent = 220,

                                        controls = [
                                            self._create_image_card(f'{self.paths[1]}/{img}') for img in self.covers
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
                                                            self.container_color_opacity,

                                                            ft.Column(
                                                                alignment = ft.MainAxisAlignment.CENTER,
                                                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                                                col = 8,

                                                                controls = [
                                                                    ft.Text(
                                                                        value = 'Regule a opacity da color',
                                                                        size = 16,
                                                                        text_align = ft.TextAlign.CENTER
                                                                    ),

                                                                    self.opacity_slider,
                                                                    
                                                                    self._create_button(
                                                                        click = 'opacity',
                                                                        col = None,
                                                                        text = 'Salvar Opacidade',
                                                                        background_color = color.azul_medio2,
                                                                        text_color = color.branco
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
                                                            self._create_color_card(color) for color in color._paleta_de_cores()
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
                            self._create_button(
                                click = 'cancel', 
                                text = 'Cancelar', 
                                col = 6,
                                background_color = color.vermelho,
                                text_color = color.branco
                            ),

                            self._create_button(
                                click = 'concluir', 
                                text = 'Concluir', 
                                col = 6,
                                background_color = color.amarelo,
                                text_color = color.preto1
                            )
                        ]
                    )
                ]
            )
        )

        if self.mode == PlalistOverlayMode.UPDATE:
            self._fill_in_fields()

    def _fill_in_fields(self):
        playlist = self.state.playlist_config  # PlaylistDetalhada

        self.state.name = playlist.name
        self.state.color = playlist.style["color"]
        self.state.opacity = playlist.style["opacity"]
        self.state.image = playlist.style["path"]
        self.state.path = playlist.musicas["path"]

        self.container_color_opacity.bgcolor = playlist.style["color"]
        self.container_color_opacity.opacity = playlist.style["opacity"]
        self.text_name.value = f"Nome da playlist: {playlist.name}"
        self.path_text.value = f"Pasta: {playlist.musicas['path']}"

    def _create_image_card(self, image):
        card = ft.Container(
            height = 220,
            width = 220,
            data = image,
            alignment = ft.alignment.top_right,
            on_click = self._select_image,
            image = ft.DecorationImage(
                src = image,
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
    
    def _create_color_card(self, color : ft.Colors):
        cont = ft.Container(
            width = 100,
            height = 100,
            border_radius = ft.border_radius.all(100),
            bgcolor = color,
            alignment = ft.alignment.center,
            data = color,
            on_click = self._select_color,

            content = ft.Text(
                value = color.replace('Colors.', '').upper(),
                text_align = ft.TextAlign.CENTER,
                weight = ft.FontWeight.W_300
            )
        )

        self.colors.append(cont)
        return cont
    
    def confirm(self, e):
        if self.mode == PlalistOverlayMode.CREATE:
            self.create_playlist()
        elif self.mode == PlalistOverlayMode.UPDATE:
            self.state.update_playlist()
            self.close_overlay(e=None)


    def _create_button(
        self, 
        click, 
        col: int, 
        text: str, 
        text_color: str, 
        background_color: str
    ) -> ft.TextButton:
        if click == 'cancel':
            click = self.close_overlay
        elif click == 'concluir':
            click = self.confirm
        elif click == 'path':
            click = self.open_selector_path
        elif click == 'opacity':
            click = self.save_opacity
        else:
            click =  None
        
        return ft.TextButton(
            col = col,
            text = text,
            on_click = click,
            height = 40,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                    ft.ControlState.HOVERED : background_color
                },
                side = {
                    ft.ControlState.HOVERED : ft.BorderSide(2, color.branco)
                },
                color = {
                    ft.ControlState.DEFAULT : color.branco,
                    ft.ControlState.HOVERED : text_color
                },
                padding = ft.padding.all(10)
            )
        )
    
    def _select_image(self, e):
        self.state.image = e.control.data

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
        self.container_color_opacity.opacity = self.opacity_slider.value
        self.container_color_opacity.update()

    def _select_color(self, e):
        self.state.color = e.control.data
        self.container_color_opacity.bgcolor = e.control.data
        self.container_color_opacity.update()
        
        for container in self.colors:
            color = container.content.value

            if container.data == e.control.data:
                container.scale = 1.1
                container.content.weight = ft.FontWeight.BOLD
            else:
                container.scale = 1.0
                container.content.weight = ft.FontWeight.W_300
            
            container.update()

    def save_opacity(self, e):
        cor_opc = ft.Colors.with_opacity(
            color = self.state.color, 
            opacity = self.container_color_opacity.opacity
        )

        self.state.color = cor_opc
        self.state.opacity = self.container_color_opacity.opacity

        self.page.open(
            ft.SnackBar(
                content = ft.Text('Valor de Opacidade Salva')
            )
        )

    def _submit_name(self, e):
        self.state.name = self.text_field.value
        self.text_name.value = f'Nome da playlist: {self.text_field.value}'
        self.text_field.value = ''
        self.update()
    
    def _change(self, e):
        self.state.name = self.text_field.value
        self.text_name.value = f'Nome da playlist: {self.text_field.value}'
        self.update()

    def open_selector_path(self, e):
        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory()
        root.destroy()
        

        if path in self.check_existing_paths():
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Já existe uma playlist com essa path de músicas, escolha outra!')
                )
            )
            self.page.update()
        else:
            self.state.path = path
            self.path_text.value = f'Pasta selecionada: {path}'
            self.path_text.update()
    
    def close_overlay(self, e):
        self.state.image = r'Assets\Global\Images\Padrao\capa_playlist_padrao.png'
        self.state.name = None
        self.state.color = '#3d3d3d'
        self.state.opacity = 1.0
        self.state.path = None
        
        self.page.overlay.clear()
        self.page.update()

    async def start_pipeline(self, path: str, id: str):
        await asyncio.to_thread(
            Pipeline.start_wrapper_sync,
            path,
            [],
            id
        )

    def check_existing_playlists(self) -> list[str]:
        return self.state.return_existngs_playlists()

    def check_existing_paths(self) -> list[str]:
        return self.state.return_existngs_folders()

    def create_playlist(self):
        if self.state.name is None:
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Atribua um name a sua playlist primeiro')
                )
            )
            self.page.update()
        elif self.state.name in self.check_existing_playlists():
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Já existe uma playlist com esse name, escolha outro!')
                )
            )
            self.page.update()
        elif self.state.path is None:
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Selecione uma path para criar')
                )
            )
            self.page.update()
        elif self.state.path in self.check_existing_paths():
            self.page.open(
                ft.SnackBar(
                    content = ft.Text('Já existe uma playlist com essa path de músicas, escolha outra!')
                )
            )
            self.page.update()
        else:
            id = self.state.create_playlist()
            self.page.run_task(
                self.start_pipeline,
                self.state.path,
                id
            )
            self.close_overlay(e = None)