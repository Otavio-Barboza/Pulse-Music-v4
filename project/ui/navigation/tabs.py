# imports da ui (interface)
from project.ui.others.colors import color
from project.ui.others.music_search import MusicSearch
from project.ui.playlist.base.base_playlists import ColumnCards
from project.ui.grid_view.grid import GridImages
from project.ui.favorite.favoritas import Favorite

# imports de back-end
from project.core.services.account_manager import AccountManager
from project.core.services.controllers.grid_state import GridMode
from project.core.services.controllers.resize_manager import ResizeManager

# import geral
import flet as ft


class TabsNavigation(ft.Tabs):
    def __init__(self):
        super().__init__(
            selected_index = 0,
            animation_duration = 300,
            label_color = color.amarelo,
            divider_color = ft.Colors.TRANSPARENT,
            indicator_color = color.amarelo,
            indicator_border_radius = ft.border_radius.all(50),
            overlay_color = color.preto8,
            unselected_label_color = color.branco_puro,
            scrollable = False,
            expand = True,
            tab_alignment = ft.TabAlignment.FILL,
            
            label_text_style = ft.TextStyle(
                size = 16,
                weight = ft.FontWeight.BOLD,
                letter_spacing = 1,
            ),

            unselected_label_text_style = ft.TextStyle(
                weight = ft.FontWeight.W_300
            )
        )
        
        self._icones_tabs = []
        self._labels_tabs = []
        self.lista_labels = [
            {'label' : 'Playlists', 'icon' : ft.Icons.MUSIC_NOTE_SHARP},
            {'label' : 'Artistas', 'icon' : ft.Icons.PERSON_SEARCH_ROUNDED}, 
            {'label' : 'Álbuns', 'icon' : ft.Icons.QUEUE_MUSIC_ROUNDED}, 
            {'label' : 'Favoritas', 'icon' : ft.Icons.FAVORITE_SHARP}, 
            {'label' : 'Pesquisar', 'icon' : ft.Icons.YOUTUBE_SEARCHED_FOR_ROUNDED}
        ]

        self.playlist = ColumnCards()
        self.pesquisa_musica = MusicSearch()
        self.artistas = GridImages(
            modo = GridMode.ARTIST,
            caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Artistas'
        )
        self.albuns = GridImages(
            modo = GridMode.ALBUM,
            caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Albuns'
        )
        
        self._criar_tabs()

        self.tabs = [
            ft.Tab(
                tab_content = self._labels_tabs[0],
                content = self.playlist                
            ),

            ft.Tab(
                tab_content = self._labels_tabs[1],
                content = self.artistas
            ),

            ft.Tab(
                tab_content = self._labels_tabs[2],
                content = self.albuns
            ),

            ft.Tab(
                tab_content = self._labels_tabs[3],
                content = None
            ),

            ft.Tab(
                tab_content = self._labels_tabs[4],
                content = self.pesquisa_musica
            ),
        ]

        ResizeManager.register(self._ajustar_tabs)

    def _criar_tabs(self):
        for l in self.lista_labels:
            label, icone = self._tab_label(
                icon=l["icon"],
                texto=l["label"]
            )

            self._labels_tabs.append(label)
            self._icones_tabs.append(icone)

    def _tab_label(self, icon, texto):
        icone = ft.Icon(icon, size = 18)

        row = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 8,
            
            controls=[
                icone,
                ft.Text(
                    texto,
                    size = 14,
                    weight = ft.FontWeight.W_700
                )
            ]
        )

        return row, icone

    def _ajustar_tabs(self, e=None):
        compact: float | int = self.page.width < 576
        
        icon: ft.Icons

        for icon in self._icones_tabs:
            icon.visible = not compact

        self.update()
        
    def atualizar_grids(self):
        self.tabs[1].content.reconstruir_imagens(
            modo = GridMode.ARTIST
        )
        self.tabs[1].update()
    
    def carregar_favoritas(self):
        from project.core.song.model.song import Song
        from project.core.favorite.controller.favoritas_controller import FavoriteState
        from project.core.song.model.reproduction import Reproduction
        from project.core.song.enum.song_enum import ReproductionMode

        list_musics: list[Song] = FavoriteState.list_favorited_objects()
        
        self.tabs[3].content = Favorite(
            list_music_object = list_musics,
            favorite_mode = ReproductionMode.FAVORITE
        )
        self.tabs[3].update()

        Reproduction.load_songs_from_mode(
            mode = ReproductionMode.FAVORITE,
            list = list_musics
        )