from project.ui.others.colors import colors
import flet as ft
import random, asyncio

class AboutSettings(ft.Container):
    def __init__(self, page):
        super().__init__(
            alignment = ft.alignment.center,
            padding = 0
        )

        self.page = page

        self._CARD_CONTENT = [
            (ft.Icons.PLAY_ARROW_ROUNDED, 'Reprodução', 'Reprodução completa no melhor estilo player clássico, com avanço automático de faixas e controle de volume — do jeitinho que um player de verdade deve ser.'),
            (ft.Icons.MUSIC_NOTE_ROUNDED, 'Playlists', 'Crie, organize e personalize suas playlists do seu jeito, porque suas músicas merecem mais do que uma bagunça aleatória.'),
            (ft.Icons.FULLSCREEN_ROUNDED, 'Tela Expandida', 'Expanda a visualização e aproveite tudo com mais conforto — letras, informações e menos esforço para enxergar.'),
            (ft.Icons.LYRICS_ROUNDED, 'letra da música', 'Gosta de acompanhar a letra da sua música? Na tela expandida, acompanhe a letra disponível para a maioria das músicas.'),
            (ft.Icons.FAVORITE_ROUNDED, 'Favoritas', 'Marque suas músicas preferidas e tenha uma reprodução separada — afinal, nem toda música merece o mesmo status.'),
            (ft.Icons.PERSON_SEARCH_ROUNDED, 'Artistas', 'Veja os artistas presentes nas suas playlists e descubra quais realmente dominam sua biblioteca musical.'),
            (ft.Icons.QUEUE_MUSIC_ROUNDED, 'Álbuns', 'Navegue pelos álbuns e veja suas faixas com organização, pouco de conhecimento a mais não dói né?.'),
            (ft.Icons.ASSISTANT_ROUNDED, 'Assistente', 'A LUNA está sempre à disposição para executar comandos por voz — menos cliques, mais música.'),
            (ft.Icons.YOUTUBE_SEARCHED_FOR_ROUNDED, 'Pesquisa Música', 'Pesquise músicas sem sair do player: informe o nome (e o artista, se quiser evitar confusão) e vá direto ao clipe no YouTube.'),
            (ft.Icons.ACCOUNT_CIRCLE_ROUNDED, 'Contas', 'Gerencie múltiplas contas no app — ideal para famílias, amigos ou pessoas que não gostam de dividir playlists.'),
            (ft.Icons.PALETTE_ROUNDED, 'Aparência Geral', 'Personalize temas e detalhes visuais do player, porque ouvir música fica melhor quando o app combina com você.'),
            (ft.Icons.SUPPORT_AGENT_ROUNDED, 'Suporte', 'Precisa de ajuda, encontrou um problema ou só quer dar aquele feedback? O suporte está sempre pronto para ouvir.'),
        ]
        self._TIPS = [
            ('Já tentou expandir o player? Às vezes a melhor parte está escondida 🫣.', colors.preto_cinza),
            ('Favoritar músicas não é só decolorsação — facilita a sua vida depois 😉', colors.preto_cinza),
            ('Se a música tiver letra... não se sinta envergonhado de cantá-la 🎶 (mesmo que errado 😅)', colors.preto_cinza),
            ('A LUNA não morde viu 😜? Pode conversar com player... você vai gostar 😉!', colors.preto_cinza),
            ('Não quer niguém de atormentando 🙄? Crie as suas playlists!', colors.preto_cinza),
            ('Cada conta tem seu espaço. Nem todo mundo precisa ouvir o mesmo gosto musical 😑', colors.preto_cinza),
            ('Procurar música no navegador é coisa do passado... 🖥️', colors.preto_cinza),
            ('Eaí já foi ver os artistas que você ouve? Não? Ta esperando o que? 🤨', colors.preto_cinza),
            ('Ei tu gosta de ver as músicas de cada álbum? Aqui gosto não importa e sim sua diversão! Vai lá ver 😉.', colors.preto_cinza),
            ('Ei! Aumenta o VOLUME aí, essa música é boa... 😌', colors.preto_cinza),
            ('Precisa de ajuda??? Calma! Não é o fim do mundo! vá ao suporte!', colors.preto_cinza),
            ('Tem preguiça de clicar em botões? Aqui a LUNA faz por você! Ah, não vire um preguiçoso, ok?', colors.preto_cinza)
        ]

        self.row_icons = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER, 
            vertical_alignment = ft.CrossAxisAlignment.END, 
            controls = []
        )
        
        self._create_icons()
        
        self.random_tips = self._TIPS[random.randint(0, len(self._TIPS) - 1)]

        self.text_tip = self._create_texts(
            texto = self.random_tips[0],
            colors_texto = colors.branco_puro,
            negrito = ft.FontWeight.BOLD,
            tamanho = 16,
            max_linhas = 2
        )

        self.container_tips = ft.Container(
            width = 800,
            height = 90,
            alignment = ft.alignment.center,
            bgcolor = self.random_tips[1],
            border_radius = ft.border_radius.all(25),
            margin = ft.margin.only(
                bottom = 20,
                top = 55
            ),
            padding = ft.padding.all(10),
            on_click = self.update_tip,

            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,

                controls = [
                    ft.ResponsiveRow(
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        controls = [self.text_tip]
                    ),
                    self.row_icons
                ]
            )
        )
        
        self.carousel = ft.Row(
            scroll = ft.ScrollMode.AUTO,
        
            controls = [
                self._criar_cards(
                    icon = item[0],
                    titulo = item[1],
                    texto = item[2]
                ) for item in self._CARD_CONTENT
            ]
        )

        self.main_content = ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            scroll = ft.ScrollMode.HIDDEN,
            expand = True,
            
            controls = [ 
                # Logo + titulo e frase
                ft.Container(
                    margin = ft.margin.only(
                        top = 5,
                        bottom = 10
                    ),

                    content = ft.ResponsiveRow(
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        width = 500,

                        controls = [
                            ft.Container(
                                col = {'md' : 3, 'xs' : 12},
                                alignment = ft.alignment.center,

                                content = ft.CircleAvatar(
                                    radius = 42,
                                    bgcolor = colors.branco,
                                    content = ft.Image(
                                        src = r'Assets\Global\Images\Logo\logo_v2.png',
                                        fit = ft.ImageFit.COVER,
                                        border_radius = ft.border_radius.all(100),
                                        filter_quality = ft.FilterQuality.HIGH
                                    ) 
                                )
                            ),

                            ft.Container(
                                col = {'md' : 6, 'xs' : 12},
                                alignment = ft.alignment.center,
                                width = 200,

                                content = ft.Column(
                                    horizontal_alignment = ft.CrossAxisAlignment.START,
                                    alignment = ft.MainAxisAlignment.START,
                                    spacing = 0,
                                    
                                    controls = [
                                        self._create_texts(
                                            texto = 'Pulse Music',
                                            colors_texto = colors.branco,
                                            negrito = ft.FontWeight.BOLD,
                                            tamanho = 36,
                                            alignment = ft.TextAlign.LEFT,
                                            fonte = 'sansita'
                                        ),
                                        self._create_texts(
                                            texto = 'A música ao seu alcance',
                                            colors_texto = colors.branco,
                                            negrito = ft.FontWeight.W_400,
                                            tamanho = 18,
                                            alignment = ft.TextAlign.LEFT
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ),

                # O que é esse projeto?
                ft.Container(
                    width = 900,
                    alignment = ft.alignment.center,
                    bgcolor = colors.preto8,
                    border_radius = ft.border_radius.all(15),
                    margin = ft.margin.only(
                        top = 20
                    ),
                    padding = ft.padding.all(15),

                    content = ft.ResponsiveRow(
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        
                        controls = [
                            ft.Container(
                                col = {'md' : 2, 'xs' : 12, 'sm' : 3.5},
                                alignment = ft.alignment.center,

                                content = ft.CircleAvatar(
                                    radius = 48,
                                    bgcolor = ft.Colors.TRANSPARENT,
                                    content = ft.Image(
                                        src = r'Assets\Global\Images\Sobre\proposta.png',
                                        fit = ft.ImageFit.COVER,
                                        border_radius = ft.border_radius.all(100)
                                    )
                                )
                            ),
                            
                            ft.Column(
                                col = {'md' : 10, 'xs' : 12, 'sm' : 8.5},
                                spacing = 7.5,
                        
                                controls = [
                                    self._create_texts(
                                        texto = 'Qual a Finidade?',
                                        colors_texto = colors.branco,
                                        negrito = ft.FontWeight.BOLD,
                                        tamanho = 30
                                    ),
                                    self._create_texts(
                                        texto = 'Pulse Music — nostalgia de um player clássico com recursos modernos.',
                                        colors_texto = colors.branco,
                                        negrito = ft.FontWeight.W_400,
                                        tamanho = 18,
                                        max_linhas = 4,
                                        alignment = ft.TextAlign.JUSTIFY
                                    )
                                ]
                            )
                        ]
                    )
                ),

                # dicas
                self.container_tips,
                
                # Carrossel das funcionalidades: o que cada uma faz?
                ft.Container(
                    width = 1400,
                    height = 300,
                    margin = ft.margin.only(
                        top = 15
                    ),
                    
                    content = ft.Column(
                        controls = [
                            self.carousel,

                            ft.Row(
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls = [
                                    ft.IconButton(
                                        icon = ft.Icons.KEYBOARD_ARROW_LEFT,
                                        on_click = self._move_carousel_left,
                                        
                                        icon_size = 25,
                                        style = ft.ButtonStyle(
                                            color = {
                                                ft.ControlState.DEFAULT : colors.branco,
                                                ft.ControlState.HOVERED : colors.roxo
                                            },
                                            bgcolor = {
                                                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                                                ft.ControlState.HOVERED : colors.branco3
                                            }
                                        )
                                    ),
                                    ft.IconButton(
                                        icon = ft.Icons.KEYBOARD_ARROW_RIGHT,
                                        on_click = self._move_carousel_right,
                                        
                                        icon_size = 25,
                                        style = ft.ButtonStyle(
                                            color = {
                                                ft.ControlState.DEFAULT : colors.branco,
                                                ft.ControlState.HOVERED : colors.roxo
                                            },
                                            bgcolor = {
                                                ft.ControlState.DEFAULT : ft.Colors.TRANSPARENT,
                                                ft.ControlState.HOVERED : colors.branco3
                                            }
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

        self.footer = ft.Container(
            height = 100,
            alignment = ft.alignment.bottom_center,
        
            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.END,

                controls = [
                    self._create_texts(
                        texto = 'Pulse Music: a nostalgia do player clássico reinventada.',
                        colors_texto = colors.branco,
                        negrito = ft.FontWeight.W_400,
                        tamanho = 20,
                        max_linhas = 2
                    ),

                    ft.Row(
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        wrap = True,
                        spacing = 6,

                        controls = [
                            self._create_texts(
                                texto = '© 2025 Pulse Music. Software desenvolvido para fins acadêmicos.',
                                colors_texto = colors.branco,
                                negrito = ft.FontWeight.W_500,
                                tamanho = 12,
                                max_linhas = 1
                            )
                        ]
                    )
                ]
            )
        )

        self.content = ft.Column(
            spacing = 0,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            
            controls = [
                self.main_content,
                self.footer  
            ]
        )
    
    def _create_texts(
            self, 
            text: str, 
            text_color: str, 
            weight: ft.FontWeight, 
            size: int, 
            overflow : ft.TextOverflow = ft.TextOverflow.FADE, 
            max_lines: int = 1, 
            alignment: ft.TextAlign = ft.TextAlign.CENTER,
            columns: int | None = None,
            font: str = 'google_sans_flex'
        ):
        """
            Função para criar os textos da tela sobre o app.

        Args:
            text (str): texto desejado colocar
            text_color (str): colors a definir para o texto
            weight (ft.FontWeight): expessura da font
            size (int): size da font
            overflow (ft.TextOverflow, optional): Encolhimento do texto conforme o espaço não existente. { Defaults to ft.TextOverflow.FADE }
            max_lines (int, optional): máximo de linhas para quebra de texto. { Defaults to 1 }
            alignment (ft.TextAlign, optional): posicionamento do texto. { Defaults to ft.TextAlign.CENTER} 
            columns (int | None, optional): columns que ocupará. { Defaults to None }

        Returns:
            ft.Text : Texto a ser atríbuido
        """
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
    
    def _criar_cards(
        self, 
        icon: ft.Icons, 
        title: str, 
        text: str
    ):
        return ft.Container(
            width = 350,
            height = 250,
            border_radius = ft.border_radius.all(15),
            padding = ft.padding.all(15),
            alignment = ft.alignment.center,
            gradient = ft.LinearGradient(
                begin = ft.alignment.top_center,
                end = ft.alignment.bottom_center,
                # colors = ["#293041", "#1a1d29"]
                colors = [colors.preto_puro_4, ft.Colors.with_opacity(1, colors.preto_puro_5), ft.Colors.with_opacity(1, colors.preto_puro_5), colors.preto_puro_4]
            ),

            content = ft.Column(
                spacing = 20,
                alignment = ft.MainAxisAlignment.CENTER,

                controls = [
                    ft.Row(
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.CENTER,

                        controls = [
                            ft.Icon(
                                name = icon,
                                color = colors.branco_puro,
                                size = 35
                            ),
                            self._create_texts(
                                text = title,
                                text_color = colors.branco_puro,
                                size = 30,
                                max_lines = 1,
                                weight = ft.FontWeight.BOLD,
                            )
                        ]
                    ),
                    self._create_texts(
                        text = text,
                        text_color = colors.branco_puro,
                        size = 18,
                        max_lines = 7,
                        weight = ft.FontWeight.W_400,
                        alignment = ft.TextAlign.JUSTIFY
                    )
                ]
            )
        )
    
    def _create_icons(self):
        for i in range(len(self._TIPS)):
            self.row_icons.controls.append(
                ft.Icon(
                    name = ft.Icons.CIRCLE,
                    size = 6,
                    data = i,
                    color = colors.branco
                )
            )
        
        self.update()
    
    def update_tip(self, *_):
        if not self.page:
            return
        
        indice = random.randint(0, len(self._TIPS) - 1)
        self.text_tip.value = self._TIPS[indice][0]
        
        for icon in self.row_icons.controls:
            icon.color = colors.amarelo4 if icon.data == indice else colors.branco

        self.container_tips.bgcolor = self._TIPS[indice][1]        
        self.update()
    
    def star_loop(self):
        if hasattr(self, '_task_dicas'):
            return
        self._task_dicas = self.page.run_task(self.loop_tips)
    
    def stop_loop(self):
        if hasattr(self, '_task_dicas'):
            self._task_dicas.cancel()
            self._task_dicas = None

    async def loop_tips(self):
        try:
            while True:
                await asyncio.sleep(10)
                if not self.page:
                    break
                self.update_tip()
        except asyncio.CancelledError:
            pass

    def _move_carousel_left(self, e):
        self.carousel.scroll_to(
            delta = -300,
            duration = 250,
            curve = ft.AnimationCurve.DECELERATE
        )
        self.update()
        
    def _move_carousel_right(self, e):
        self.carousel.scroll_to(
            delta = 300,
            duration = 250,
            curve = ft.AnimationCurve.DECELERATE
        )
        self.update()