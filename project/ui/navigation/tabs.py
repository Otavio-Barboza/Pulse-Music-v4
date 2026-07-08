from project.ui.others.colors import color
from project.ui.others.music_search import MusicSearch
from project.ui.playlist.base.base_playlists import ColumnCards
from project.ui.grid_view.grid import GridImages
from project.ui.favorite.favoritas import Favorite
from ...App.Services.Controllers.estado_redimensionamento import ResizeManager
from ...App.Services.Controllers.estado_grid import GridMode
from ...App.Services.gerenciador_contas import GerenciadorContas
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

        self.playlist = ColumnCards(page = self.page)
        self.pesquisa_musica = MusicSearch(page = self.page)
        self.artistas = GridImages(
            modo = GridMode.ARTISTA,
            caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Artistas',
            page = self.page
        )
        self.albuns = GridImages(
            modo = GridMode.ALBUM,
            caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Albuns',
            page = self.page
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

        ResizeManager.registrar(self._ajustar_tabs)

    def _criar_tabs(self):
        for l in self.lista_labels:
            label, icone = self._tab_label(
                icon=l["icon"],
                texto=l["label"]
            )

            self._labels_tabs.append(label)
            self._icones_tabs.append(icone)

    def _tab_label(self, icon, texto):
        icone = ft.Icon(icon, size=18)

        row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            
            controls=[
                icone,
                ft.Text(
                    texto,
                    size=14,
                    weight=ft.FontWeight.W_700
                )
            ]
        )

        return row, icone

    def _ajustar_tabs(self, e=None):
        compacto = self.page.width < 576

        for icone in self._icones_tabs:
            icone.visible = not compacto

        self.update()
        
    def atualizar_grids(self):
        self.tabs[1].content.reconstruir_imagens(
            modo = GridMode.ARTISTA
        )
        self.tabs[1].update()
    
    def carregar_favoritas(self):
        from ...App.Favoritas.Controller.favoritas_controller import EstadoFavoritas
        from ...App.Audio.Model.modo_reproducao import Reprodução, ModoReprodução
        
        lista_de_musicas = EstadoFavoritas.listar_objetos_favoritados()
        self.tabs[3].content = Favorite(
            page = self.page,
            lista_objetos_musica = lista_de_musicas,
            caminho = ModoReprodução.FAVORITA
        )
        self.tabs[3].update()

        Reprodução.carregar_musicas_do_modo(
            modo = ModoReprodução.FAVORITA,
            lista = lista_de_musicas
        )