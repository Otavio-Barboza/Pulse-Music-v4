from ....App.Audio.Controller.estado_musica import EstadoMusica
from ...Others.cores import cor
import flet as ft

class RowContainer(ft.Container):
    def __init__(self, page, musica, tipagem : str):
        super().__init__(
            border_radius = ft.border_radius.all(10),
            height = 55,
            bgcolor = cor.preto9,
            padding = ft.padding.all(5),
            alignment = ft.alignment.center,
            data = musica,
            on_click = self.tocar_ou_pausar
        )
        self.page = page
        self.musica = musica
        self.tipagem = tipagem

        self.icon = ft.IconButton(
            icon = ft.Icons.FAVORITE,
        
            style = ft.ButtonStyle(
                color = cor.rosa_avermelhado,

                overlay_color = {
                    ft.ControlState.HOVERED : cor.cinza2
                }
            )
        )

        self.imagem = ft.Image(
            src = r'Assets\Data\Contas\113676693738175180594\Imagens\Capa Musica\Blessed (Avicii Radio Edit)(MP3_320K).jpg',
            border_radius = ft.border_radius.all(5),
            fit = ft.ImageFit.COVER,
            filter_quality = ft.FilterQuality.MEDIUM,
            height = 47.5,
            width = 80
        )

        self.musica = self._retornar_nomes(nome = self.musica.nome, tamanho = 900)
        self.artista = self._retornar_nomes(nome = 'Nome do Artista', tamanho = 300)
        
        self.content = ft.Row(
            spacing = 40,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.SPACE_AROUND,

            controls = [
                self.icon,
                self.imagem,

                ft.Row(
                    wrap = True,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.START,
                    run_alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 10,
                    run_spacing = 1,
                    expand = True,
                    
                    controls = [
                        self.musica,
                        self.artista
                    ]
                )
            ]
        )

    def _retornar_nomes(self, nome : str, tamanho : int):
        return ft.Text(
            value = nome,
            size = 15,
            weight = ft.FontWeight.W_500,
            overflow = ft.TextOverflow.ELLIPSIS,
            max_lines = 1,
            text_align = ft.TextAlign.LEFT,
            width = tamanho
        )
    
    def tocar_ou_pausar(self, e):
        EstadoMusica.definir_musica_atual(e.control.data)