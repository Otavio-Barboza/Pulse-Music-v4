from ....App.Audio.Controller.sessao import SessaoReproducao
from Assets.Interface.Others.cores import cor
import flet as ft

class InfosExpandida(ft.Container):
    def __init__(self, page):
        super().__init__(
            col = {'md' : 5, 'sm' : 12},
            alignment = ft.alignment.center,
            padding = ft.padding.all(10),
        )
        self.page = page

        self.imagem = ft.Container(
            col = 12,
            padding = ft.padding.all(10),
            content = self._adicionar_img()
        )

        self.content = ft.Column(
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.ResponsiveRow(
                    controls = [
                        self.imagem
                    ]
                )
            ]
        )

        SessaoReproducao.registrar_callback('musica_atual', self.att_infos_expandido)
    
    def _criar_textos(self, valor : str = '') -> ft.Text:
        return ft.Text(
            value = valor
        )
    
    def _adicionar_img(self, img : str = r'Assets\Global\Images\Padrao\capa_musicas_desconhecidas.png') -> ft.Image:
        return ft.Image(
            src = img,
            border_radius = ft.border_radius.all(10),
            fit = ft.ImageFit.CONTAIN,
            filter_quality = ft.FilterQuality.HIGH,
            height = 300,
            width = 600
        )
    
    def att_infos_expandido(self, dados = None):
        self.imagem.content.src = SessaoReproducao.buscar_capa()
        self.update()