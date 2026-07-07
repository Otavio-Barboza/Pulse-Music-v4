# imports de interface
from project.ui.others.colors import color

# imports gerais
import asyncio, pywhatkit
import flet as ft


class MusicSearch(ft.Container):
    def __init__(self):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )

        self._EXAMPLE_LIST: list[str] = [
            'Ex: Infinity - Guru Josh',
            'Ex: Imagine Dragons - Believer',
            'Ex: Coldplay - Yellow',
            'Ex: Queen - Bohemian Rhapsody',
            'Ex: Linkin Park - Numb'
        ]

        self.text_field = ft.TextField(
            hint_text = 'Digite a music...',
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
            on_submit = self.submit_music
        )

        self.container_text = ft.Container(
            alignment = ft.alignment.center_left,
            width = 700,

            margin = ft.margin.only(
                top = 20,
                bottom = 15
            ),

            content = self._create_text(
                text = 'Ex:',
                size = 20,
                text_color = color.branco2,
                max_lines = 1,
                weight = ft.FontWeight.W_300
            )
        )

        self.content = ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.Container(
                    content = self._create_text(
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
    
    def _create_text(
            self, 
            text : str, 
            text_color : str, 
            weight : ft.FontWeight, 
            size : int, 
            overflow : ft.TextOverflow = ft.TextOverflow.FADE, 
            max_lines : int = 1, 
            alignment : ft.TextAlign = ft.TextAlign.CENTER,
            columns : int | None = None,
            font : str = 'inter'
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
            alignment (ft.TextAlign, optional): posicionamento do text. { Defaults to ft.TextAlign.CENTER} 
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
            text_align = alignment,
            col = columns,
            font_family = font
        )
    
    async def animation_example(self):
        previous: str = ''

        while True:
            for example in self._EXAMPLE_LIST:
                for i in range(len(example)):
                    current = example[i]

                    if len(previous) == len(example) - 1:
                        previous = ''
                    else:
                        previous += current
                    
                    self.container_text.content.value = previous
                    self.container_text.update()
                        
                    await asyncio.sleep(0.4)
            
    def start_animation(self):
        self.page.run_task(self.animation_example)

    def search(self, music):
        try:
            pywhatkit.playonyt(music)
            return True
        except Exception as erro:
            print(erro)
            return False

    def submit_music(self, e):
        name: str = self.text_field.value
        result: bool = self.search(name)
        
        if result:
            self.page.open(ft.SnackBar(
                ft.Text(f'Música {name} encontrada com sucesso!')
            ))
            self.text_field.value = ''
            self.text_field.update()
            self.page.update()
        else:
            self.page.open(ft.SnackBar(
                ft.Text(f'Música {name} não encontrada, tente novamente!')
            ))
            self.page.update()