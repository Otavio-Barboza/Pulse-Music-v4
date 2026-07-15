# import de interface
from ui.others.colors import color

# import de back-end
from core.services.controllers.state_app import StateApp
from core.playlists.controller.playlist_state import PlaylistState
from core.favorite.controller.favoritas_controller import FavoriteState
from core.favorite.enum.favorite_enum import Favorited
from core.song.enum.song_enum import ReproductionMode
from core.song.model.reproduction import Reproduction
from core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class RowContainer(ft.Container):
    def __init__(
            self, 
            musica, 
            status_favoritada
        ):
        super().__init__(
            border_radius = ft.border_radius.all(10),
            height = 55,
            bgcolor = color.preto9,
            padding = ft.padding.all(5),
            alignment = ft.alignment.center,
            data = musica,
            on_click = self.tocar_ou_pausar
        )

        self._esta_favoritado = status_favoritada
        self.imagem_capa = self.encontrar_capa()

        self.icon = ft.IconButton(
            data = musica,
            icon = self.esta_favoritada(),

            style = ft.ButtonStyle(
                color = color.rosa_avermelhado,

                overlay_color = {
                    ft.ControlState.HOVERED : color.cinza2
                }
            ),
            
            on_click = self.toogle_favoritar 
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

        StateApp.register_callback(
            event = 'actualization_artist',
            func = self.atualizar_atistas
        )
        StateApp.register_callback(
            event = 'actualization_cover',
            func = self.atualizar_capas
        )

    def will_unmount(self):
        StateApp._callbacks['actualization_artist'].remove(self._callback_artistas)
        StateApp._callbacks['actualization_cover'].remove(self._callback_capas)

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
    
    def esta_favoritada(self):          
        if self._esta_favoritado == Favorited.NOT_FAVORITED:
            return ft.Icons.FAVORITE_ROUNDED
        else:
            return ft.Icons.HEART_BROKEN_ROUNDED

    def att_icon(self):
        self._esta_favoritado = Favorited.NOT_FAVORITED
        self.icon.icon = ft.Icons.HEART_BROKEN_ROUNDED
        self.icon.update()
    
    def att_icon_favoritado(self):
        self._esta_favoritado = Favorited.FAVORITED
        self.icon.icon = ft.Icons.FAVORITE_ROUNDED
        self.icon.update()
    
    def toogle_favoritar(self, e):        
        if self._esta_favoritado == Favorited.FAVORITED:
            self._esta_favoritado = Favorited.NOT_FAVORITED
            self.icon.icon = ft.Icons.HEART_BROKEN_ROUNDED
            self.desfavoritar(e.control.data)
        else:
            self._esta_favoritado = Favorited.FAVORITED
            self.icon.icon = ft.Icons.FAVORITE
            self.favoritar(e.control.data)

        if self.page:
            self.icon.update()
        
    def favoritar(self, data):
        FavoriteState.convert_object_to_json(data)
        FavoriteState.add_music_to_playback(data)
        ReproductionManager.update_queues()

    def desfavoritar(self, data):
        FavoriteState.remove_favorite_json(data)
        FavoriteState.remove_music_to_playback(data)
        ReproductionManager.update_queues()

    def tocar_ou_pausar(self, e):
        if Reproduction.current_reproduction != e.control.data.modo:
            if e.control.data.modo == ReproductionMode.FAVORITE.value:
                Reproduction.set_current_reproduction(ReproductionMode.FAVORITE)
            else:
                Reproduction.set_current_reproduction(e.control.data.modo)
        
        if ReproductionManager.fonte_atual != e.control.data.modo:
            ReproductionManager.set_font()

        if ReproductionManager.current_font is ReproductionMode.NOT_REPRODUCE:
            print('Sem reprodução definida')
            return

        ReproductionManager.receber_indice(e.control.data.chave)
        ReproductionManager.tocar_indice()

    def encontrar_artista(self) -> str:
        return PlaylistState.return_music_artist(self.data.chave)
    
    def encontrar_capa(self) -> str:
        return PlaylistState.return_cover(self.data.nome)
    
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