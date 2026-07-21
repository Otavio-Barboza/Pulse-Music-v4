# imports de interface
from ui.others.colors import color
from ui.player_section.controls.icons import PlayerIcons
from ui.player_section.controls.command import PlayerCommands
from ui.player_section.controls.information import PlayerInformation
from ui.player_section.controls.progress_bar import CompactProgressBar
from ui.player_section.controls.expanded_information import ExpandedInformation
from ui.player_section.controls.navigation.expanded_menu import InformationMenu
from ui.player_section.controls.navigation.content import ContentInformation
from ui.player_section.controls.navigation.content_lyrics import LyricsContainer
from ui.player_section.controls.navigation.translation_content import TranslationContent

# imports de back-end
from core.services.controllers.estado_section import StateSection
from core.services.controllers.resize_manager import ResizeManager

# import geral
import flet as ft


class PlayerSection:

    def __init__(self, page: ft.Page):
        self.page = page
        self.overlays = []
        
        self.progress_bar_compact = None
        self.progress_bar_expanded = None
       
        self.information_compact = None
        self.information_expanded = None
        
        self.icons_compact = None
        self.icons_expanded = None
        
        self.commands_compact = None
        self.commands_expanded = None
        
        self.compact = None
        self.compact_expanded = None
        
        self.expanded_information = None
        self.menu_information = None
        self.information_content = None
        
        self.expanded = None

        ResizeManager.register(self._resize)


    # CRIAÇÃO DE COMPONENTES DA CLASSE
    def _create_components(self):
        # progress bar
        self.progress_bar_compact = CompactProgressBar(self.page)
        self.progress_bar_expanded = CompactProgressBar(self.page)

        # informações do compact
        self.information_compact = PlayerInformation(self.page)
        self.information_expanded = PlayerInformation(self.page)

        # icones do compact
        self.icons_compact = PlayerIcons(page = self.page)
        self.icons_expanded = PlayerIcons(page = self.page)

        # comandos do compact
        self.commands_compact = PlayerCommands(page = self.page, expanded = self.expanded, player = self)
        self.commands_expanded = PlayerCommands(page = self.page, expanded = self.expanded, player = self)

        # compact
        self.compact = self._create_compact(expanded = False)
        self.compact_expanded = self._create_compact(expanded = True)

        self.expanded_information = ExpandedInformation(self.page)
        self.menu_information = InformationMenu(page = self.page, trocar_view = self._alter_view)

        self.expanded = ft.Container(
            bgcolor = color.preto2,
            visible = False,

            content = ft.Column(
                spacing = 0,

                controls = [
                    self._expanded_md() if self.page.width < 768 else self._expanded_sm(),
                    self.compact_expanded
                ]
            )
        )


    # INICIALIZAÇÃO DA CLASSE
    def load(self):
        self._create_components()
        # self.page.update()

    def connect(self):
        ResizeManager.register(self._resize)


    # criação dos itens 
    def _create_compact(self, expanded: bool) -> ft.Container:
        return ft.Container(
            height = 220,
            bgcolor = color.preto7,
            alignment = ft.alignment.center,
            border_radius = ft.border_radius.only(
                top_left = 10,
                top_right = 10
            ),
            
            content = ft.Column(
                spacing = 0,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,

                controls = [
                    self.progress_bar_compact if not expanded else self.progress_bar_expanded,

                    ft.ResponsiveRow(
                        spacing = 0,
                        run_spacing = 7.5,
                        vertical_alignment = ft.MainAxisAlignment.CENTER,
                        expand = True,

                        controls = [self.information_expanded, self.icons_expanded, self.commands_expanded] if expanded else [self.information_compact, self.icons_compact, self.commands_compact]
                    )
                ]
            )
        )
    
    def expanded(self, e):
        self.expanded.visible = not self.expanded.visible
        self.information_expanded.imagem.visible = False

        if not self.expanded.visible:
            self.commands_expanded.icon_expandir.icon = ft.Icons.FULLSCREEN
            self.commands_compact.icon_expandir.icon = ft.Icons.FULLSCREEN
        else:
            self.commands_compact.icon_expandir.icon = ft.Icons.FULLSCREEN_EXIT
            self.commands_expanded.icon_expandir.icon = ft.Icons.FULLSCREEN_EXIT
            
        self._alter_view('lyric')
        self.page.update()

    def minimized(self, e):
        self.expanded.visible = False
        self.page.update()
    
    def register_overlay(self, overlay):
        self.overlays.append(overlay)
        self.page.overlay.append(overlay)
    
    def close_overlay(self):
        for o in self.overlays:
            o.visible = False
    
    def _alter_view(self, view):
        if view == 'lyric':
            self.information_content.trocar(LyricsContainer(page = self.page))
        elif view == 'translation':
            self.information_content.trocar(TranslationContent(page = self.page))
        
        StateSection.alter_view('view', view)
        self.page.update()

        # print("CONTEUDO INFOS PAGE FINAL", self.information_content.page)
    
    def _expanded_md(self) -> ft.ResponsiveRow:
        return ft.Column(
            expand = True,

            controls = [
                self.menu_information,

                ft.ResponsiveRow(
                    expand = True,
                    spacing = 0,

                    controls = [
                        self.expanded_information,
                        
                        ft.Column(
                            col = 7,
                            expand = True,
                            controls = [self.content_information_menu_scrolavel(columns = 7)]
                        )
                    ]
                )
            ]
        )
    
    def _expanded_sm(self) -> ft.Column:
        return ft.Column(
            expand = True,
            spacing = 0,

            controls = [
                self.menu_information,
                self.expanded_information,
                self.content_information_menu_scrolavel(columns = 12)
            ]
        )
    
    def content_information_menu_scrolavel(self, columns : int) -> ft.Column:
        self.information_content = ContentInformation()
        return ft.Container(
            col = columns,
            expand = True,
            content = self.information_content,
            alignment = ft.alignment.center
        )
    
    def _resize(self, e = None): 
        # print("CONTEUDO INFOS PAGE ANTES", self.information_content.page)

        self.expanded.content.controls.clear()

        # print("CONTEUDO INFOS PAGE DEPOIS CLEAR", self.information_content.page)

        if self.page.width < 768:
            self.expanded.content.controls.append(self._expanded_sm())
        else:
            self.expanded.content.controls.append(self._expanded_md())
        
        self.expanded.content.controls.append(self.compact_expanded)
        
        self._alter_view(StateSection.state['view'])
        self.expanded.update()
        