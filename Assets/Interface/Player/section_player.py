from ..Others.cores import cor
from .Controls.infos import InfoPlayer
from .Controls.icones import IconsPlayer
from .Controls.comando import ComandosPlayer
from .Controls.barra_duracao import BarraDuracaoCompacta
from .Controls.infos_expandido import InfosExpandida
from .Controls.Navigation.menu_expandido import MenuInfos
from .Controls.Navigation.conteudo import ConteudoInfos
from .Controls.Navigation.conteudo_letra import ContainerLetra
from ...App.Services.Controllers.estado_section import EstadoSection
from ...App.Services.Controllers.estado_redimensionamento import ResizeManager
import flet as ft

class PlayerSection:
    def __init__(self, page):
        self.page = page
        self.overlays = []
        
        self.barra_duração_compacta = BarraDuracaoCompacta(page = self.page)
        self.barra_duração_expandida = BarraDuracaoCompacta(page = self.page)
        
        self.info_compacto = InfoPlayer(page = self.page)
        self.info_espandido = InfoPlayer(page = self.page)
        self.icones_compacto = IconsPlayer(page = self.page)
        self.icones_expandido = IconsPlayer(page = self.page)
        self.comandos_compacto = ComandosPlayer(page = self.page, expandir = self.expandir, player = self)
        self.comandos_expandido = ComandosPlayer(page = self.page, expandir = self.expandir, player = self)
        
        self.compacto = self._retornar_compacto(expandido = False)
        self.compacto_expandido = self._retornar_compacto(expandido = True)

        self.info_expandido = InfosExpandida(page = self.page)
        self.menu_infos = MenuInfos(page = self.page, trocar_view = self._trocar_view)
        self.conteudo_infos = ConteudoInfos()
        
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
            
        EstadoSection.alterar('view', 'info')
        self._trocar_view('info')
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
            self.conteudo_infos.trocar(ContainerLetra())
        elif view == 'info':
            self.conteudo_infos.trocar(ft.Container(expand = True, bgcolor = cor.azul_escuro, content = ft.Text('value')))
        elif view == 'artista':
            self.conteudo_infos.trocar(ft.Container(expand = True, bgcolor = cor.roxo, content = ft.Text('value')))
        
        EstadoSection.alterar('view', view)
        self.page.update()
    
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
        return ft.Container(
            col = colunas,
            expand = True,
            content = self.conteudo_infos
        )
    
    def _redimensionar(self, e  = None):
        self.expandido.content.controls.clear()

        if self.page.width < 768:
            self.expandido.content.controls.append(self._expandido_SM())
        else:
            self.expandido.content.controls.append(self._expandido_MD())
        
        self.expandido.content.controls.append(self.compacto_expandido)

        self.expandido.update()