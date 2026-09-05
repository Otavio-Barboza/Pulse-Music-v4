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
        
        self.information_content_desktop = None
        self.information_content_mobile = None
        
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
        self.commands_compact = PlayerCommands(page = self.page, expanded = self._expanded, player = self)
        self.commands_expanded = PlayerCommands(page = self.page, expanded = self._expanded, player = self)

        # compact
        self.compact = self._create_compact(expanded = False)
        self.compact_expanded = self._create_compact(expanded = True)


        # Tela expandida
        self.expanded_information_desktop = ExpandedInformation(self.page)
        self.expanded_information_mobile = ExpandedInformation(self.page)

        self.menu_information_desktop = InformationMenu(page = self.page, alter_view = self._alter_view)
        self.menu_information_mobile = InformationMenu(page = self.page, alter_view = self._alter_view)

        self.expanded_scream_desktop = self._expanded_md()
        self.expanded_scream_mobile = self._expanded_sm()

        self.expanded = ft.Container(
            bgcolor = color.preto2,
            visible = False,

            content = ft.Column(
                spacing = 0,

                controls = [
                    self.expanded_scream_desktop,
                    self.expanded_scream_mobile,
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
    
    def _expanded(self, e):
        from core.services.controllers.state_app import StateApp

        self.expanded.visible = not self.expanded.visible
        self.expanded_scream_mobile.visible = False
        self.information_expanded.image_cover.visible = False
        
        if not self.expanded.visible:
            self.commands_expanded.expand_icon.icon = ft.Icons.FULLSCREEN
            self.commands_compact.expand_icon.icon = ft.Icons.FULLSCREEN

            StateApp.expanded_section_is_open = False
        else:
            self.commands_compact.expand_icon.icon = ft.Icons.FULLSCREEN_EXIT
            self.commands_expanded.expand_icon.icon = ft.Icons.FULLSCREEN_EXIT

            StateApp.expanded_section_is_open = True

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
            self.information_content_mobile.to_replace(LyricsContainer(page = self.page))
            self.information_content_desktop.to_replace(LyricsContainer(page = self.page))
        elif view == 'translation':
            self.information_content_desktop.to_replace(TranslationContent(page = self.page))
            self.information_content_mobile.to_replace(TranslationContent(page = self.page))
        
        StateSection.alter_view('view', view)
        self.page.update()

    
    def _expanded_md(self) -> ft.ResponsiveRow:
        return ft.Column(
            expand = True,

            controls = [
                self.menu_information_desktop,

                ft.ResponsiveRow(
                    expand = True,
                    spacing = 0,

                    controls = [
                        self.expanded_information_desktop,
                        
                        ft.Column(
                            col = 7,
                            expand = True,
                            controls = [self.content_information_menu_scrolavel(
                                columns = 7, plataform = True
                            )]
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
                self.menu_information_mobile,
                self.expanded_information_mobile,
                self.content_information_menu_scrolavel(
                    columns = 12, plataform = False
                )
            ]
        )
    
    def content_information_menu_scrolavel(self, columns: int, plataform: bool) -> ft.Column:
        if plataform:
            self.information_content_desktop = ContentInformation(self.page)
        else:
            self.information_content_mobile = ContentInformation(self.page)

        return ft.Container(
            col = columns,
            expand = True,
            content = self.information_content_desktop if plataform else self.information_content_mobile,
            alignment = ft.alignment.center
        )
    
    def _resize(self, e = None): 
        from core.services.controllers.state_app import StateApp

        if StateApp.expanded_section_is_open:
            if self.page.width < 768:
                self.expanded_scream_desktop.visible = False
                self.expanded_scream_mobile.visible = True
            else:
                self.expanded_scream_mobile.visible = False
                self.expanded_scream_desktop.visible = True
            
            self._alter_view(StateSection.state['view'])
            self.page.update()
        