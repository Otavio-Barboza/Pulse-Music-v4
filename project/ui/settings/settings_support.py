# import de interface
from ui.others.colors import color
from ui.utils.utils_ui import UtilsUi

# imports de back-end
from core.services.email_service import send_email
from core.services.account_manager import AccountManager

# import geral
import flet as ft


class SettingsSupport(ft.Container):
    def __init__(self):
        super().__init__(
            expand = True
        )

        self.text_field = ft.TextField(
            hint_text = 'Digite a mensagem...',
            hint_style = ft.TextStyle(
                color = color.cinza1,
                size = 16
            ),

            border_radius = ft.border_radius.all(12),
            max_length = 1600,
            min_lines = 2,
            max_lines = 4,
            multiline = True,
            height = 150,
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
                                    bgcolor = color.branco,
                                    content = ft.Image(
                                        src = r'Assets\Global\Images\Logo\logo_v2.png',
                                        border_radius = ft.border_radius.all(100),
                                        filter_quality = ft.FilterQuality.HIGH,
                                        fit = ft.ImageFit.COVER
                                    )
                                ),
                                self._create_texts(
                                    text = 'Suporte Pulse Music',
                                    text_color = color.branco_puro,
                                    weight = ft.FontWeight.BOLD,
                                    size = 48,
                                    max_lines = 2
                                )
                            ]
                        ),
                    
                        ft.Container(
                            margin = ft.margin.only(
                                top = 30,
                                bottom = 15
                            ),
                    
                            content = self._create_texts(
                                text = '→  Aqui você possui o suporte do que necessitar referente ao app. Envie dúvidas, problemas ou feedbacks. \n→   Basta digitar a mensagem na caixa de text e para confirmar, clique em salvar.',
                                text_color = color.branco_puro,
                                weight = ft.FontWeight.W_400,
                                size = 20,
                                max_lines = 7,
                                alignment = ft.TextAlign.JUSTIFY
                            )
                        ),    
                    
                        self.text_field,
                    
                        ft.Container(
                            margin = ft.margin.only(
                                top = 10,
                                bottom = 25
                            ),

                            content = ft.Column(
                                controls = [
                                    self._create_texts(
                                        text = ' E-mail do suporte: barbozaotavio17@gmail.com',
                                        text_color = color.branco_puro,
                                        weight = ft.FontWeight.W_400,
                                        size = 18,
                                        max_lines = 5,
                                        alignment = ft.TextAlign.JUSTIFY
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
                                    on_click = self.send,

                                    style = ft.ButtonStyle(
                                        bgcolor = {
                                            ft.ControlState.DEFAULT : color.amarelo,
                                            ft.ControlState.HOVERED : color.amarelo2
                                        },

                                        padding = ft.padding.all(10),
                                        color = color.preto_puro_5,
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
    
    def _create_texts(
            self, 
            text : str, 
            text_color : str, 
            weight : ft.FontWeight, 
            size : int, 
            overflow : ft.TextOverflow = ft.TextOverflow.FADE, 
            max_lines : int = 1, 
            alignment : ft.TextAlign = ft.TextAlign.CENTER,
            columns : int | None = None
        ):
        """
            Função para criar os textos da tela sobre o app.

        Args:
            text (str): text desejado colocar
            text_color (str): color a definir para o text
            weight (ft.FontWeight): expessura da fonte
            size (int): size da fonte
            overflow (ft.TextOverflow, optional): Encolhimento do text conforme o espaço não existente. { Defaults to ft.TextOverflow.FADE }
            max_lines (int, optional): máximo de linhas para quebra de text. { Defaults to 1 }
            alignment (ft.TextAlign, optional): posicionamento do text. { Defaults to ft.TextAlign.CENTER} 
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
            col = columns
        )
    
    def send(self, e):
        message = self.text_field.value.strip()
        
        if len(message) > 1500:
            UtilsUi.snack_bar("A mensagem pode ter no máximo 1000 caracteres.")
            return
        
        if not message:
            UtilsUi.snack_bar("Digite uma mensagem antes de enviar 😅")
            return
        
        try:
            email_user = AccountManager.user().email

            send_email(
                message = message,
                email_user = email_user
            )

            self.text_field.value = ''
            self.text_field.update()

            UtilsUi.snack_bar("Mensagem enviada com sucesso! 📬")
        except Exception as err:
            UtilsUi.snack_bar("Erro ao enviar mensagem 😬")
            print("Erro ao enviar e-mail:", err)