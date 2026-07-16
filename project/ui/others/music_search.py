# import de interface
from ui.others.colors import color

# imports gerais
import asyncio, pywhatkit
import flet as ft


class MusicSearch(ft.Container):
    def __init__(self, page):
        super().__init__(
            expand = True,
            padding = ft.padding.all(10)
        )
        self.page = page
        self.lista_ex = [
            'Ex: Infinity - Guru Josh',
            'Ex: Imagine Dragons - Believer',
            'Ex: Coldplay - Yellow',
            'Ex: Queen - Bohemian Rhapsody',
            'Ex: Linkin Park - Numb'
        ]

        self.caixa_texto = None
        self.container_texto = None
        self.content = None

    
    # FUNÇÕES DE CRIAÇÃO DE COMPONENTES
    def _create_components(self):
        self.caixa_texto = ft.TextField(
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
            on_submit = self._submeter_musica
        )

        self.container_texto = ft.Container(
            alignment = ft.alignment.center_left,
            width = 700,
            margin = ft.margin.only(
                top = 20,
                bottom = 15
            ),
            content = self._criar_textos(
                texto = 'Ex:',
                tamanho = 20,
                color_texto = color.branco2,
                max_linhas = 1,
                negrito = ft.FontWeight.W_300
            )
        )

    def _build_class(self):
        self.content = ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.Container(
                    content = self._criar_textos(
                        texto = 'Pesquisar Música no YouTube',
                        color_texto = color.amarelo4,
                        negrito = ft.FontWeight.BOLD,
                        tamanho = 50
                    )
                ),
            
                self.container_texto,
                self.caixa_texto
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
            texto : str, 
            color_texto : str, 
            negrito : ft.FontWeight, 
            tamanho : int, 
            overflow : ft.TextOverflow = ft.TextOverflow.FADE, 
            max_linhas : int = 1, 
            alinhamento : ft.TextAlign = ft.TextAlign.CENTER,
            colunas : int | None = None,
            fonte : str = 'inter'
        ):
        '''
            Função para criar os textos da tela sobre o app.

        Args:
            texto (str): texto desejado colocar
            color_texto (str): color a definir para o texto
            negrito (ft.FontWeight): expessura da fonte
            tamanho (int): tamanho da fonte
            overflow (ft.TextOverflow, optional): Encolhimento do texto conforme o espaço não existente. { Defaults to ft.TextOverflow.FADE }
            max_linhas (int, optional): máximo de linhas para quebra de texto. { Defaults to 1 }
            alinhamento (ft.TextAlign, optional): posicionamento do texto. { Defaults to ft.TextAlign.CENTER} 
            colunas (int | None, optional): colunas que ocupará. { Defaults to None }

        Returns:
            ft.Text : Texto a ser atríbuido
        '''
        return ft.Text(
            value = texto,
            color = color_texto,
            weight = negrito,
            size = tamanho,
            overflow = overflow,
            max_lines = max_linhas,
            text_align = alinhamento,
            col = colunas,
            font_family = fonte
        )
    
    async def animacao_ex(self):
        anterior = ''

        while True:
            for letra in self.lista_ex:
                for i in range(len(letra)):
                    atual = letra[i]

                    if len(anterior) == len(letra) - 1:
                        anterior = ''
                    else:
                        anterior += atual
                    
                    self.container_texto.content.value = anterior
                    self.container_texto.update()
                        
                    await asyncio.sleep(0.4)
            
    def iniciar_animacao(self):
        self.page.run_task(self.animacao_ex)

    def pesquisar(self, musica):
        try:
            pywhatkit.playonyt(musica)
            return True
        except Exception as erro:
            print(erro)
            return False

    def _submeter_musica(self, e):
        nome = self.caixa_texto.value
        resultado = self.pesquisar(nome)
        
        if resultado:
            self.page.open(ft.SnackBar(
                ft.Text(f'Música {nome} encontrada com sucesso!')
            ))
            self.caixa_texto.value = ''
            self.caixa_texto.update()
            self.page.update()
        else:
            self.page.open(ft.SnackBar(
                ft.Text(f'Música {nome} não encontrada, tente novamente!')
            ))
            self.page.update()