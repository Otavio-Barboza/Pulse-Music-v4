from project.ui.others.colors import color
from project.ui.player_section.controls.information import PlayerInformation
from project.ui.player_section.controls.icons import PlayerIcons
from project.ui.player_section.controls.command import PlayerCommands
from project.ui.player_section.controls.progress_bar import CompactProgressBar
from project.ui.player_section.controls.expanded_information import ExpandedInformation
from project.ui.player_section.controls.navigation.expanded_menu import InformationMenu
from project.ui.player_section.controls.navigation.content import ContentInformation
from project.ui.player_section.controls.navigation.content_lyrics import LyricsContainer
from project.ui.player_section.controls.navigation.translation_content import TranslationContent
from ...App.Services.Controllers.estado_section import EstadoSection
from ...App.Services.Controllers.estado_redimensionamento import ResizeManager
import flet as ft

class PlayerSection:

    def __init__(self):
        self.overlays = []
        
        self.barra_duração_compacta = CompactProgressBar(page = self.page)
        self.barra_duração_expandida = CompactProgressBar(page = self.page)
        
        self.info_compacto = PlayerInformation(page = self.page)
        self.info_espandido = PlayerInformation(page = self.page)
        self.icones_compacto = PlayerIcons(page = self.page)
        self.icones_expandido = PlayerIcons(page = self.page)
        self.comandos_compacto = PlayerCommands(page = self.page, expandir = self.expandir, player = self)
        self.comandos_expandido = PlayerCommands(page = self.page, expandir = self.expandir, player = self)
        
        self.compacto = self._retornar_compacto(expandido = False)
        self.compacto_expandido = self._retornar_compacto(expandido = True)

        self.info_expandido = ExpandedInformation(page = self.page)
        self.menu_infos = InformationMenu(page = self.page, trocar_view = self._trocar_view)
        self.conteudo_infos = None
        
        self.expandido = ft.Container(
            bgcolor = cor.preto2,
            visible = False,

            content = ft.Column(
                spacing = 0,

                controls = [
                    self._expandido_MD() if self.page.width < 768 else self._expandido_SM(),
                    self.compacto_expandido
                ]
            )
        )

        ResizeManager.registrar(self._redimensionar)

    def _retornar_compacto(self, expandido : bool) -> ft.Container:
        return ft.Container(
            height = 220,
            bgcolor = cor.preto7,
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
                    self.barra_duração_compacta if not expandido else self.barra_duração_expandida,

                    ft.ResponsiveRow(
                        spacing = 0,
                        run_spacing = 7.5,
                        vertical_alignment = ft.MainAxisAlignment.CENTER,
                        expand = True,

                        controls = [self.info_espandido, self.icones_expandido, self.comandos_expandido] if expandido else [self.info_compacto, self.icones_compacto, self.comandos_compacto]
                    )
                ]
            )
        )
    
    def expandir(self, e):
        self.expandido.visible = not self.expandido.visible
        self.info_espandido.imagem.visible = False

        if not self.expandido.visible:
            self.comandos_expandido.icon_expandir.icon = ft.Icons.FULLSCREEN
            self.comandos_compacto.icon_expandir.icon = ft.Icons.FULLSCREEN
        else:
            self.comandos_compacto.icon_expandir.icon = ft.Icons.FULLSCREEN_EXIT
            self.comandos_expandido.icon_expandir.icon = ft.Icons.FULLSCREEN_EXIT
            
        self._trocar_view('letra')
        self.page.update()

    def minimizar(self, e):
        self.expandido.visible = False
        self.page.update()
    
    def registrar_overlay(self, overlay):
        self.overlays.append(overlay)
        self.page.overlay.append(overlay)
    
    def fechar_overlay(self):
        for o in self.overlays:
            o.visible = False
    
    def _trocar_view(self, view):
        if view == 'letra':
            self.conteudo_infos.trocar(LyricsContainer())
        elif view == 'traducao':
            self.conteudo_infos.trocar(TranslationContent())
        
        EstadoSection.alterar('view', view)
        self.page.update()

        # print("CONTEUDO INFOS PAGE FINAL", self.conteudo_infos.page)
    
    def _expandido_MD(self) -> ft.ResponsiveRow:
        return ft.Column(
            expand = True,

            controls = [
                self.menu_infos,

                ft.ResponsiveRow(
                    expand = True,
                    spacing = 0,

                    controls = [
                        self.info_expandido,
                        
                        ft.Column(
                            col = 7,
                            expand = True,
                            controls = [self._conteudo_infos_menu_scrolavel(colunas = 7)]
                        )
                    ]
                )
            ]
        )
    
    def _expandido_SM(self) -> ft.Column:
        return ft.Column(
            expand = True,
            spacing = 0,

            controls = [
                self.menu_infos,
                self.info_expandido,
                self._conteudo_infos_menu_scrolavel(colunas = 12)
            ]
        )
    
    def _conteudo_infos_menu_scrolavel(self, colunas : int) -> ft.Column:
        self.conteudo_infos = ContentInformation()
        return ft.Container(
            col = colunas,
            expand = True,
            content = self.conteudo_infos,
            alignment = ft.alignment.center
        )
    
    def _redimensionar(self, e = None): 
        # print("CONTEUDO INFOS PAGE ANTES", self.conteudo_infos.page)

        self.expandido.content.controls.clear()

        # print("CONTEUDO INFOS PAGE DEPOIS CLEAR", self.conteudo_infos.page)

        if self.page.width < 768:
            self.expandido.content.controls.append(self._expandido_SM())
        else:
            self.expandido.content.controls.append(self._expandido_MD())
        
        self.expandido.content.controls.append(self.compacto_expandido)
        
        self._trocar_view(EstadoSection._estado['view'])
        self.expandido.update()
        