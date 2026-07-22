# import de interface
from ui.others.colors import color
from ui.utils.utils_ui import UtilsUi

# imports gerais
import asyncio, pywhatkit
import flet as ft


class MusicSearch(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )
        self.page = page
        self.example_list = [
            'Ex: Infinity - Guru Josh',
            'Ex: Imagine Dragons - Believer',
            'Ex: Coldplay - Yellow',
            'Ex: Queen - Bohemian Rhapsody',
            'Ex: Linkin Park - Numb'
        ]
        self._stop = False
        self.text_field = None
        self.container_text = None
        self.content = None

    
    # FUNÇÕES DE CRIAÇÃO DE COMPONENTES
    def _create_components(self):
        self.text_field = ft.TextField(
            hint_text = 'Digite a musica...',
            hint_style = ft.TextStyle(
                color = color.cinza1,
                size = 16
            ),

            border_radius = ft.border_radius.all(12),
            max_length = 1000,
            multiline = False,
            height = 100,
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
            on_submit = self._submit_music_name
        )

        self.container_text = ft.Container(
            alignment = ft.alignment.center_left,
            width = 700,
            margin = ft.margin.only(
                top = 20,
                bottom = 15
            ),
            content = self._criar_textos(
                text = 'Ex:',
                size = 20,
                text_color = color.branco2,
                max_lines = 1,
                weight = ft.FontWeight.W_300
            )
        )

    def _build_class(self):
        self.content = ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.Container(
                    content = self._criar_textos(
                        text = 'Pesquisar Música no YouTube',
                        text_color = color.amarelo4,
                        weight = ft.FontWeight.BOLD,
                        size = 50
                    )
                ),
            
                self.container_text,
                self.text_field
            ]
        )
    

    # FUNÇÃO DE INICIALIZAÇÃO
    def load(self):
        self._create_components()
        self._build_class()
        # self.update()


    # CRIAÇÃO DE ITENs
    def _criar_textos(
        self, 
        text: str, 
        text_color: str, 
        weight: ft.FontWeight, 
        size: int, 
        overflow: ft.TextOverflow = ft.TextOverflow.FADE, 
        max_lines: int = 1, 
        aligment: ft.TextAlign = ft.TextAlign.CENTER,
        columns: int | None = None,
        font: str = 'inter'
    ):
        '''
            Função para criar os textos da tela sobre o app.

        Args:
            text (str): text desejado colocar
            text_color (str): color a definir para o text
            weight (ft.FontWeight): expessura da font
            size (int): size da font
            overflow (ft.TextOverflow, optional): Encolhimento do text conforme o espaço não existente. { Defaults to ft.TextOverflow.FADE }
            max_lines (int, optional): máximo de linhas para quebra de text. { Defaults to 1 }
            aligment (ft.TextAlign, optional): posicionamento do text. { Defaults to ft.TextAlign.CENTER} 
            columns (int | None, optional): columns que ocupará. { Defaults to None }

        Returns:
            ft.Text : Texto a ser atríbuido
        '''
        return ft.Text(
            value = text,
            color = text_color,
            weight = weight,
            size = size,
            overflow = overflow,
            max_lines = max_lines,
            text_align = aligment,
            col = columns,
            font_family = font
        )
    
    async def example_animation(self):
        anterior = ''

        while self._stop != True:
            for letra in self.example_list:
                for i in range(len(letra)):
                    atual = letra[i]

                    if len(anterior) == len(letra) - 1:
                        anterior = ''
                    else:
                        anterior += atual
                    
                    self.container_text.content.value = anterior
                    self.container_text.update()
                        
                    await asyncio.sleep(0.4)

    def stop_animation(self):
        self._stop = True

    def start_animation(self):
        self.page.run_task(self.example_animation)

    def search(self, musica):
        try:
            pywhatkit.playonyt(musica)
            return True
        except Exception as erro:
            print(erro)
            return False

    def _submit_music_name(self, e):
        name = self.text_field.value
        result = self.search(name)
        
        if result:
            UtilsUi.snack_bar(
                text = f"Música {name} encontrada com sucesso!",
                page = self.page
            )
            self.text_field.value = ''
            self.text_field.update()
            self.text_field.update()
        else:
            UtilsUi.snack_bar(
                text = f"Música {name} não encontrada, tente novamente!",
                page = self.page
            )