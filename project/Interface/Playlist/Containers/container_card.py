from ....App.Playlists.Controller.estado_playlist import EstadoPlay
from Assets.Interface.Others.cores import cor
import flet as ft

class CardPlaylist(ft.Container):
    def __init__(
            self, 
            page, 
            on_abrir, 
            on_remover, 
            carregar_playlist,
            playlist_id : str, 
            nome : str, 
            qtde_musicas : int,
            cor_fundo : str | ft.Colors,
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
        self.page = page
        self.nome_playlist = nome
        self.qtde_musicas = str(qtde_musicas)
        self.playlist_id = playlist_id
        self.cor_fundo = cor_fundo
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
            icon_color = cor.preto3,
            surface_tint_color = cor.branco,
            bgcolor = cor.preto3,
            shadow_color = cor.branco,
            tooltip = "Mais opções",

            style = ft.ButtonStyle(
                bgcolor = ft.Colors.TRANSPARENT,
                overlay_color = cor.amarelo
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
            bgcolor = self.cor_fundo,

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

        EstadoPlay.registar_callback(
            evento = 'att_qtde_play',
            funcao = self.alterar_qtde_de_musicas_playlist
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
        callbacks = EstadoPlay._callbacks.get('att_qtde_play', [])
        
        if self.alterar_qtde_de_musicas_playlist in callbacks:
            callbacks.remove(
                self.alterar_qtde_de_musicas_playlist
            )