from ...Others.cores import cor
from ..Containers.container_card import CardPlaylist
import flet as ft

class GridPlaylists(ft.GridView):
    def __init__(self, page, on_abrir, on_remover, carregar_musicas):
        super().__init__(
            max_extent = 270,
            spacing = 12,
            run_spacing = 12,
            clip_behavior = ft.ClipBehavior.NONE
        )
        self.page = page
        self.on_abrir = on_abrir
        self.on_remover = on_remover
        self.carregar_musicas = carregar_musicas
        self.cards = {}
    
    def adicionar_playlist(
        self, 
        playlist_id : str, 
        nome : str, 
        qtde_mus : int,
        cor : str | ft.Colors,
        img : str,
        path : str
    ):
        card = CardPlaylist(
            page = self.page,
            playlist_id = playlist_id,
            nome = nome,
            qtde_musicas = qtde_mus,
            cor_fundo = cor,
            imagem_fundo = img,
            pasta = path,
            on_abrir = lambda e: self.on_abrir(playlist_id),
            on_remover = lambda e: self.on_remover(playlist_id),
            carregar_playlist = lambda e: self.carregar_musicas(playlist_id, path)
        )

        if self.cards.get(playlist_id, None) is None:
            self.cards[playlist_id] = card
            self.controls.append(card)
            self.update()
    
    def atualizar_playlist(
        self,
        playlist_id: str,
        nome: str,
        cor: str | ft.Colors,
        img: str,
        path: str,
        qtde_mus: int | None = None
    ):
        card = self.cards.get(playlist_id)

        if not card:
            return  # segurança

        # Atualiza dados básicos
        card.nome_play.value = nome
        card.imagem.content.src = img
        card.container_info.bgcolor = cor
        card.pasta = path
        card.data['pasta'] = path

        # print(card.data)
        if qtde_mus is not None:
            card.qtde.value = f"{qtde_mus} músicas"

        card.update()