# imports de interface
from project.ui.others.colors import color
from project.ui.others.music_search import MusicSearch
from project.ui.playlist.base.base_playlists import ColumnCards
from project.ui.grid_view.grid import GridImages
from project.ui.favorite.favoritas import Favorite

# imports de back-end
from project.core.services.controllers.resize_manager import ResizeManager
from project.core.services.controllers.grid_state import GridMode
from project.core.services.account_manager import AccountManager

# import gertal
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
        
        self._tabs_icons = []
        self._labels_tabs = []
        self.label_list = [
            {'label' : 'Playlists', 'icon' : ft.Icons.MUSIC_NOTE_SHARP},
            {'label' : 'Artistas', 'icon' : ft.Icons.PERSON_SEARCH_ROUNDED}, 
            {'label' : 'Álbuns', 'icon' : ft.Icons.QUEUE_MUSIC_ROUNDED}, 
            {'label' : 'Favoritas', 'icon' : ft.Icons.FAVORITE_SHARP}, 
            {'label' : 'Pesquisar', 'icon' : ft.Icons.YOUTUBE_SEARCHED_FOR_ROUNDED}
        ]

        self.playlist = ColumnCards()
        
        self.music_search = MusicSearch()
        
        self.artist = GridImages(
            modo = GridMode.ARTIST,
            caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Artistas',
        )
        
        self.album = GridImages(
            modo = GridMode.ALBUM,
            caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Albuns',
        )
        
        self._create_tabs()

        self.tabs = [
            ft.Tab(
                tab_content = self._labels_tabs[0],
                content = self.playlist                
            ),

            ft.Tab(
                tab_content = self._labels_tabs[1],
                content = self.artist
            ),

            ft.Tab(
                tab_content = self._labels_tabs[2],
                content = self.album
            ),

            ft.Tab(
                tab_content = self._labels_tabs[3],
                content = None
            ),

            ft.Tab(
                tab_content = self._labels_tabs[4],
                content = self.music_search
            ),
        ]

        ResizeManager.register(self._tabs_resize)

    def _create_tabs(self):
        for l in self.label_list:
            label, icon = self._tab_label(
                icon_label = l["icon"],
                text = l["label"]
            )

            self._labels_tabs.append(label)
            self._tabs_icons.append(icon)

    def _tab_label(self, icon_label: ft.Icons, text: str):
        icon = ft.Icon(icon_label, size = 18)

        row = ft.Row(
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 8,
             
            controls = [
                icon,

                ft.Text(
                    text,
                    size = 14,
                    weight = ft.FontWeight.W_700
                )
            ]
        )

        return row, icon

    def _tabs_resize(self, e = None):
        compact = self.page.width < 576

        for icon in self._tabs_icons:
            icon.visible = not compact

        self.update()
        
    def update_grids(self):
        self.tabs[1].content.reconstruir_imagens(
            modo = GridMode.ARTIST
        )
        self.tabs[1].update()
    
    def load_favorites(self):
        from ...App.Favoritas.Controller.favoritas_controller import EstadoFavoritas
        from ...App.Audio.Model.modo_reproducao import Reprodução, ModoReprodução
        
        music_list = EstadoFavoritas.listar_objetos_favoritados()
        
        self.tabs[3].content = Favorite(
            list_object_music = music_list,
            path = ModoReprodução.FAVORITA
        )
        self.tabs[3].update()

        Reprodução.carregar_musicas_do_modo(
            modo = ModoReprodução.FAVORITA,
            lista = music_list
        )