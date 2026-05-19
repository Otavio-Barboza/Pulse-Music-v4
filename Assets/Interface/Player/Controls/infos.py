from ....App.Audio.Controller.sessao import EstadoMusica
from Assets.Interface.Others.cores import cor
import flet as ft

class InfoPlayer(ft.Container):
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
        self.nome_musica = self._nomes(nome = 'Música não selecionada')
        self.nome_artista = self._nomes(nome = 'Música não selecionada')

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

        EstadoMusica.registrar_callback('musica_atual', self.att_infos)
    
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
            color = cor.branco_puro
        )
    
    def att_infos(self, estado : EstadoMusica):
        self.nome_artista.value = f'Artista: {estado.musica_atual.artista}'
        self.nome_musica.value = estado.musica_atual.nome
        # self.imagem.content.src = estado.musica_atual.capa
        self.update()