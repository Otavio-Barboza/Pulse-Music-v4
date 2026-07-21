# import de back-end
from core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class ExpandedInformation(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            col = {'md' : 5, 'sm' : 12},
            alignment = ft.alignment.center,
            padding = ft.padding.all(10),
        )
        self.page = page

        self._image = ft.Container(
            col = 12,
            padding = ft.padding.all(10),
            content = self._add_image()
        )

        self.content = ft.Column(
            alignment = ft.MainAxisAlignment.CENTER,

            controls = [
                ft.ResponsiveRow(
                    controls = [
                        self._image
                    ]
                )
            ]
        )

        ReproductionManager.register_callback('current_song', self.actualization_expanded_information)
    
    def _create_text(self, value: str = '') -> ft.Text:
        return ft.Text(
            value = value
        )
    
    def _add_image(self, img: str = r'assets\images\placeholders\capa_musicas_desconhecidas.png') -> ft.Image:
        return ft.Image(
            src = img,
            border_radius = ft.border_radius.all(10),
            fit = ft.ImageFit.CONTAIN,
            filter_quality = ft.FilterQuality.HIGH,
            height = 300,
            width = 600
        )
    
    def actualization_expanded_information(self, *_):
        self._image.content.src = ReproductionManager.get_cover()
        
        if self.page:
            self.update()