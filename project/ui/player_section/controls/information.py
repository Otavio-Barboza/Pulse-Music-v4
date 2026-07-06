from ....App.Audio.Controller.sessao import SessaoReproducao
from project.ui.others.colors import color
import flet as ft

class PlayerInformation(ft.Container):
    def __init__(self, page):
        super().__init__(
            col = {'sm' : 12, 'md' : 4},
            alignment = ft.alignment.center_right,
            padding = ft.padding.only(left = 10)
        )
        self.page = page
        
        self.imagem = ft.Container(
            height = 64,
            width = 128,
            col = {'xs' : 0, 'sm' : 3},
            visible = True,
            content = self._criar_img()
        )
        self.nome_musica = self._nomes(nome = '')
        self.nome_artista = self._nomes(nome = '')

        self.content = ft.ResponsiveRow( 
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            
            controls = [
                self.imagem,

                ft.Column(
                    col = 9,
                    alignment = ft.MainAxisAlignment.CENTER,

                    controls = [
                        self.nome_musica,
                        self.nome_artista
                    ]
                )
            ]
        )

        SessaoReproducao.registrar_callback('musica_atual', self.att_infos)
    
    def _criar_img(self, img : str = r'Assets\Global\Images\Padrao\img_64_padrão.png') -> ft.Image:
        return ft.Image(
            src = img,
            border_radius = ft.border_radius.all(15),
            fit = ft.ImageFit.CONTAIN,
            filter_quality = ft.FilterQuality.HIGH
        )
    
    def _nomes(self, nome : str) -> ft.Text:
        return ft.Text(
            value = nome,
            size = 18,
            weight = ft.FontWeight.W_300,
            max_lines = 1,
            overflow = ft.TextOverflow.FADE,
            color = color.branco_puro
        )
    
    def att_infos(self, dados = None):
        self.nome_artista.value = SessaoReproducao.buscar_artista()
        self.nome_musica.value = SessaoReproducao.estado.musica_atual.nome
        self.imagem.content.src = SessaoReproducao.buscar_capa()
        self.update()