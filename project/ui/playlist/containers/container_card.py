# import de interface
from project.ui.others.colors import color

# import de back-end
from project.core.services.controllers.state_app import StateApp

# import geral
import flet as ft


class PlaylistCard(ft.Container):
    def __init__(
            self, 
            on_abrir, 
            on_remover, 
            carregar_playlist,
            playlist_id : str, 
            nome : str, 
            qtde_musicas : int,
            color_fundo : str | ft.Colors,
            imagem_fundo : str,
            pasta : str | None,
            opacidade : float = 1.0
        ):
        super().__init__(
            height = 270,
            width = 270,
            border_radius = ft.border_radius.all(20),
            scale = 1.0,
            data = {"id" : playlist_id, "pasta" : pasta},
            animate = ft.Animation(200, ft.AnimationCurve.SLOW_MIDDLE),
            on_hover = self._hover,
        )

        self.nome_playlist = nome
        self.qtde_musicas = str(qtde_musicas)
        self.playlist_id = playlist_id
        self.color_fundo = color_fundo
        self.imagem_fundo = imagem_fundo
        self.opacidade = opacidade
        self.pasta = pasta
        self.on_abrir = on_abrir
        self.on_remover = on_remover
        self.carregar_playlist = carregar_playlist
        self.on_click = lambda e: self.carregar_playlist(playlist_id)

        self.imagem = ft.Container(
            width = 270,
            expand = True,

            content = ft.Image(
                src = self.imagem_fundo,
                fit = ft.ImageFit.COVER
            )
        )
        self.nome_play = self._retornar_textos(self.nome_playlist)
        self.qtde = self._retornar_textos(f'{self.qtde_musicas} músicas')

        self.infos = ft.PopupMenuButton(
            icon = ft.Icons.MORE_VERT_ROUNDED,
            icon_color = color.preto3,
            surface_tint_color = color.branco,
            bgcolor = color.preto3,
            shadow_color = color.branco,
            tooltip = "Mais opções",

            style = ft.ButtonStyle(
                bgcolor = ft.Colors.TRANSPARENT,
                overlay_color = color.amarelo
            ),

            items = [
                ft.PopupMenuItem(
                    text = "Configurações Playlist",
                    data = nome,
                    on_click = self.on_abrir
                ),

                ft.PopupMenuItem(
                    text = "Excluir Playlist",
                    data = nome,                                        
                    on_click = self.on_remover
                )
            ]
        )

        self.container_info = ft.Container(
            height = 60,
            bgcolor = self.color_fundo,

            padding = ft.padding.only(
                top = 5,
                left = 10,
                right = 10,
                bottom = 10
            ),

            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,

                controls = [
                    ft.Column(
                        spacing = 3,

                        controls = [
                            self.nome_play,
                            self.qtde
                        ]
                    ),

                    self.infos
                ]
            )
        )

        self.content = ft.Column(
            spacing = 0,

            controls = [
                self.imagem,
                self.container_info
            ]
        )

        StateApp.register_callback(
            event = 'actualization_number_songs_of_playlist',
            func = self.alterar_qtde_de_musicas_playlist
        )

    def alterar_qtde_de_musicas_playlist(self, quantidade : dict):
        if not self.page:
            return
        
        if quantidade["id"] == self.data["id"]:
            self.qtde.value = f'{quantidade["qtde"]} músicas'
            
        try:
            self.update()
        except AssertionError as ase:
            print(ase)
            return
            
    def _retornar_textos(self, texto : str) -> ft.Text:
        return ft.Text(
            value = texto,
            size = 16,
            overflow = ft.TextOverflow.FADE,
            color = '#ffffff',
            max_lines = 1
        )
    
    def _hover(self, e : ft.HoverEvent):
        self.scale = 1.075 if e.data == 'true' else 1.0
        self.opacity = 0.8 if e.data == 'true' else 1.0
        self.update()

    def dispose(self):
        callbacks = StateApp._callbacks.get('actualization_number_songs_of_playlist', [])
        
        if self.alterar_qtde_de_musicas_playlist in callbacks:
            callbacks.remove(
                self.alterar_qtde_de_musicas_playlist
            )