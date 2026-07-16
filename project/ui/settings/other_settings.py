# import de interface
from ui.others.colors import color

# imports de back-end
from core.services.account_manager import StateApp
from core.services.settings.service_settings import ServiceSettings

# import geral
import flet as ft


class OtherSettings(ft.Container):
    def __init__(self, page):
        super().__init__(
            alignment = ft.alignment.center
        )
        self.page = page
        self.switch = ft.Switch(
            label = 'Ativar dicas',
            value = ServiceSettings.load_overlay(),
            on_change = self._switch_value_changed,
            active_track_color = color.preto_puro_5,
            inactive_track_color = color.branco,
            active_color = color.amarelo4,
            inactive_thumb_color = color.preto1,
            label_position = ft.LabelPosition.RIGHT,
            
            label_style = ft.TextStyle(
                size = 18
            )
        )

        self.content = ft.Column(
            controls = [
                self._text(
                    text = 'Dicas e informações gerais do App.',
                    tamanho = 20
                ),
                self.switch        
            ]
        )

        StateApp.register_callback('atualization_switch', self.change_switch)

    def _text(self, text: str, tamanho: int):
        return ft.Text(
            value = text,
            size = tamanho
        )
    
    def _switch_value_changed(self, e):
        self.switch.value = e.control.value
        self.update()

        StateApp.notify(event = "overlay_tips", data = e.control.value)
        StateApp.notify(event = "atualization_on_click", data = e.control.value)
    
    def change_switch(self, value: bool):
        self.switch.value = value
        self.update()