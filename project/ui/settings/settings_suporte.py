from Assets.Interface.Others.cores import cor
from Assets.App.Services.email_service import enviar_email_suporte
from Assets.App.Services.gerenciador_contas import GerenciadorContas
import flet as ft

class SettingsSuporte(ft.Container):
    def __init__(self, page):
        super().__init__(
            expand = True
            )

        self.page = page
        self.caixa_texto = ft.TextField(
            hint_text = 'Digite a mensagem...',
            hint_style = ft.TextStyle(
                color = cor.cinza1,
                size = 16
            ),

            border_radius = ft.border_radius.all(12),
            max_length = 1600,
            min_lines = 2,
            max_lines = 4,
            multiline = True,
            height = 150,
            filled = True,
            fill_color = cor.preto4,
            border_color = ft.Colors.TRANSPARENT,
            width = 700,
            
            label_style = ft.TextStyle(
                color = cor.branco
            ),
            
            text_style = ft.TextStyle(
                color = cor.branco,
                size = 16
            ),

            cursor_color = cor.amarelo,
            content_padding = ft.Padding(16, 10, 16, 10)
        )

        self.content = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Container(
                width = 700,
                height = 1000,
                alignment = ft.alignment.center,
                padding = ft.padding.all(20),
                border_radius = ft.border_radius.all(10),

                content = ft.Column(
                    spacing = 10,
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                    controls = [
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            wrap = True,
                            controls = [
                                ft.CircleAvatar(
                                    radius = 40,
                                    bgcolor = cor.branco,
                                    content = ft.Image(
                                        src = r'Assets\Global\Images\Logo\logo_v2.png',
                                        border_radius = ft.border_radius.all(100),
                                        filter_quality = ft.FilterQuality.HIGH,
                                        fit = ft.ImageFit.COVER
                                    )
                                ),
                                self._criar_textos(
                                    texto = 'Suporte Pulse Music',
                                    cor_texto = cor.branco_puro,
                                    negrito = ft.FontWeight.BOLD,
                                    tamanho = 48,
                                    max_linhas = 2
                                )
                            ]
                        ),
                    
                        ft.Container(
                            margin = ft.margin.only(
                                top = 30,
                                bottom = 15
                            ),
                    
                            content = self._criar_textos(
                                texto = '→  Aqui você possui o suporte do que necessitar referente ao app. Envie dúvidas, problemas ou feedbacks. \n→   Basta digitar a mensagem na caixa de texto e para confirmar, clique em salvar.',
                                cor_texto = cor.branco_puro,
                                negrito = ft.FontWeight.W_400,
                                tamanho = 20,
                                max_linhas = 7,
                                alinhamento = ft.TextAlign.JUSTIFY
                            )
                        ),    
                    
                        self.caixa_texto,
                    
                        ft.Container(
                            margin = ft.margin.only(
                                top = 10,
                                bottom = 25
                            ),

                            content = ft.Column(
                                controls = [
                                    self._criar_textos(
                                        texto = ' E-mail do suporte: barbozaotavio17@gmail.com',
                                        cor_texto = cor.branco_puro,
                                        negrito = ft.FontWeight.W_400,
                                        tamanho = 18,
                                        max_linhas = 5,
                                        alinhamento = ft.TextAlign.JUSTIFY
                                    )
                                ]
                            )
                        ),
                    
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            height = 50,
                            controls = [
                                ft.TextButton(
                                    text = 'Enviar mensagem',
                                    icon = ft.Icons.SEND_ROUNDED,
                                    width = 200,
                                    height = 50,
                                    on_click = self.enviar_email,

                                    style = ft.ButtonStyle(
                                        bgcolor = {
                                            ft.ControlState.DEFAULT : cor.amarelo,
                                            ft.ControlState.HOVERED : cor.amarelo2
                                        },

                                        padding = ft.padding.all(10),
                                        color = cor.preto_puro_5,
                                        shape = ft.RoundedRectangleBorder(radius = 20),
                                        alignment = ft.alignment.center,
                                        text_style = ft.TextStyle(
                                            size = 16,
                                            weight = ft.FontWeight.BOLD
                                        )
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )
    
    def _criar_textos(
            self, 
            texto : str, 
            cor_texto : str, 
            negrito : ft.FontWeight, 
            tamanho : int, 
            overflow : ft.TextOverflow = ft.TextOverflow.FADE, 
            max_linhas : int = 1, 
            alinhamento : ft.TextAlign = ft.TextAlign.CENTER,
            colunas : int | None = None
        ):
        """
            Função para criar os textos da tela sobre o app.

        Args:
            texto (str): texto desejado colocar
            cor_texto (str): cor a definir para o texto
            negrito (ft.FontWeight): expessura da fonte
            tamanho (int): tamanho da fonte
            overflow (ft.TextOverflow, optional): Encolhimento do texto conforme o espaço não existente. { Defaults to ft.TextOverflow.FADE }
            max_linhas (int, optional): máximo de linhas para quebra de texto. { Defaults to 1 }
            alinhamento (ft.TextAlign, optional): posicionamento do texto. { Defaults to ft.TextAlign.CENTER} 
            colunas (int | None, optional): colunas que ocupará. { Defaults to None }

        Returns:
            ft.Text : Texto a ser atríbuido
        """
        return ft.Text(
            value = texto,
            color = cor_texto,
            weight = negrito,
            size = tamanho,
            overflow = overflow,
            max_lines = max_linhas,
            text_align = alinhamento,
            col = colunas
        )
    
    def enviar_email(self, e):
        mensagem = self.caixa_texto.value.strip()
        print(len(mensagem))
        
        if len(mensagem) > 1500:
            self.page.open(
                ft.SnackBar(
                   ft.Text("A mensagem pode ter no máximo 1000 caracteres.")
                )
            )
            self.page.update()
            return
        
        if not mensagem:
            self.page.open(ft.SnackBar(
                ft.Text("Digite uma mensagem antes de enviar 😅")
            ))
            # self.page.snack_bar.open = True
            self.page.update()
            return
        
        try:
            email_usuario = GerenciadorContas.usuario().email

            enviar_email_suporte(
                mensagem = mensagem,
                email_usuario = email_usuario
            )

            self.caixa_texto.value = ''
            self.caixa_texto.update()

            self.page.open(ft.SnackBar(
                ft.Text("Mensagem enviada com sucesso! 📬")
            ))
            # self.page.snack_bar.open = True
            self.page.update()
        except Exception as err:
            self.page.open(ft.SnackBar(
                ft.Text("Erro ao enviar mensagem 😬")
            ))
            # self.page.snack_bar.open = True
            self.page.update()

            print("Erro ao enviar e-mail:", err)