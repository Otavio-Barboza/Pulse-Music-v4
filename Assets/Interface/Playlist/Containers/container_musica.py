from ....App.Playlists.Controller.estado_playlist import EstadoPlay
from ...Others.cores import cor
import flet as ft

class RowContainer(ft.Container):
    def __init__(
            self, 
            page, 
            musica, 
        ):
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
        self.imagem_capa = self.encontrar_capa()

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
            src = self.imagem_capa,
            border_radius = ft.border_radius.all(5),
            fit = ft.ImageFit.COVER,
            filter_quality = ft.FilterQuality.MEDIUM,
            height = 47.5,
            width = 80
        )

        self.txt_musica = self._retornar_nomes(
            nome = self.data.nome, 
            tamanho = 900
        )
        self.txt_artista = self._retornar_nomes(
            nome = self.encontrar_artista(), 
            tamanho = 300
        )
        
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
                        self.txt_musica,
                        self.txt_artista
                    ]
                )
            ]
        )

        self._callback_artistas = self.atualizar_atistas
        self._callback_capas = self.atualizar_capas

        EstadoPlay.registar_callback(
            evento = 'att_artista',
            funcao = self.atualizar_atistas
        )
        EstadoPlay.registar_callback(
            evento = 'att_capa',
            funcao = self.atualizar_capas
        )

    def will_unmount(self):
        EstadoPlay._callbacks['att_artista'].remove(self._callback_artistas)
        EstadoPlay._callbacks['att_capa'].remove(self._callback_capas)

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
        from ....App.Audio.Model.modo_reproducao import Reprodução
        from ....App.Audio.Controller.sessao import SessaoReproducao
        from ....App.Audio.Model.modo_reproducao import ModoReprodução
        
        Reprodução.definir_modo(e.control.data.modo)

        if SessaoReproducao.fonte_atual != e.control.data.modo:
            SessaoReproducao.definir_fonte()

        if SessaoReproducao.fonte_atual is ModoReprodução.SEM_REPRODUCAO:
            print('Sem reprodução definida')
            return
        
        SessaoReproducao.receber_indice(e.control.data.chave)
        SessaoReproducao.tocar_indice()

    def encontrar_artista(self) -> str:
        from ....App.Playlists.Controller.estado_playlist import EstadoPlay
        return EstadoPlay.retornar_artista_musica(self.data.chave)
    
    def encontrar_capa(self) -> str:
        from ....App.Playlists.Controller.estado_playlist import EstadoPlay
        return EstadoPlay.retornar_capa_musica(self.data.nome)
    
    def atualizar_atistas(self, _):
        nome_artista = self.encontrar_artista()
        self.txt_artista.value = nome_artista
        
        try:
            if self.page:
                self.txt_artista.update()
        except Exception as e:
            print(f'CALLBACK ARTISTAS ATT ERROR: {e}')

    def atualizar_capas(self, _):
        caminho_capa = self.encontrar_capa()
        self.imagem.src = caminho_capa
        
        try:
            if self.page:
                self.imagem.update()
        except Exception as e:
            print(f'CALLBACK CAPAS ATT ERROR: {e}')