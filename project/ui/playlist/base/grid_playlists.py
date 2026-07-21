# imports de interface
from ui.others.colors import color
from ui.playlist.containers.container_card import PlaylistCard

# import de ui
import flet as ft


class GridPlaylists(ft.GridView):
    def __init__(self, on_open, on_remove, load_songs):
        super().__init__(
            max_extent = 270,
            spacing = 12,
            run_spacing = 12,
            clip_behavior = ft.ClipBehavior.NONE
        )

        self.on_open = on_open
        self.on_remove = on_remove
        self.load_songs = load_songs
        self.cards = {}
    
    def adicionar_playlist(
        self, 
        playlist_id : str, 
        name : str, 
        qtde_mus : int,
        color : str | ft.Colors,
        img : str,
        path : str
    ):
        card = PlaylistCard(
            page = self.page,
            playlist_id = playlist_id,
            name = name,
            number_of_songs = qtde_mus,
            backgroud_color = color,
            backgroud_image = img,
            path = path,
            on_open = lambda e: self.on_open(playlist_id),
            on_remove = lambda e: self.on_remove(playlist_id),
            load_playlist = lambda e: self.load_songs(playlist_id, path)
        )

        if self.cards.get(playlist_id, None) is None:
            self.cards[playlist_id] = card
            self.controls.append(card)
            self.update()
    
    def update_playlist(
        self,
        playlist_id: str,
        name: str,
        color: str | ft.Colors,
        img: str,
        path: str,
        qtde_mus: int | None = None
    ):
        card = self.cards.get(playlist_id)

        if not card:
            return  # segurança

        # Atualiza dados básicos
        card.name_play.value = name
        card._image.content.src = img
        card.container_information.bgcolor = color
        card.path = path
        card.data['pasta'] = path

        if qtde_mus is not None:
            card.qtde.value = f"{qtde_mus} músicas"

        card.update()