# import de interface
from ui.others.colors import color

# import de back-end
from core.song.controller.reproduction_manager import ReproductionManager

# import geral
import flet as ft


class PlayerInformation(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(
            col = {'sm' : 12, 'md' : 4},
            alignment = ft.alignment.center_right,
            padding = ft.padding.only(left = 10)
        )
        self.page = page
        
        self.image_cover = ft.Container(
            height = 64,
            width = 128,
            col = {'xs' : 0, 'sm' : 3},
            visible = True,
            content = self._create_images()
        )
        self.song_name = self._create_text(name = '')
        self.artist_name = self._create_text(name = '')

        self.content = ft.ResponsiveRow( 
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            
            controls = [
                self.image_cover,

                ft.Column(
                    col = 9,
                    alignment = ft.MainAxisAlignment.CENTER,

                    controls = [
                        self.song_name,
                        self.artist_name
                    ]
                )
            ]
        )

        ReproductionManager.register_callback('current_song', self.actualization_information)
    
    def _create_images(self, img: str = r'assets\images\placeholders\img_64_padrão.png') -> ft.Image:
        return ft.Image(
            src = img,
            border_radius = ft.border_radius.all(15),
            fit = ft.ImageFit.CONTAIN,
            filter_quality = ft.FilterQuality.HIGH
        )
    
    def _create_text(self, name: str) -> ft.Text:
        return ft.Text(
            value = name,
            size = 18,
            weight = ft.FontWeight.W_300,
            max_lines = 1,
            overflow = ft.TextOverflow.FADE,
            color = color.branco_puro
        )
    
    def actualization_information(self, *_):
        self.artist_name.value = ReproductionManager.get_artist()
        self.song_name.value = ReproductionManager.state.current_song.name
        self.image_cover.content.src = ReproductionManager.get_cover()
        self.update()