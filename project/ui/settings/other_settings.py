# import de interface
from project.ui.others.colors import colors

# imports de back-end
from project.core.services.account_manager import StateApp
from project.core.services.settings.service_settings import ServiceSettings

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
            on_change = self._mudou_valor_switch,
            active_track_color = colors.preto_puro_5,
            inactive_track_color = colors.branco,
            active_color = colors.amarelo4,
            inactive_thumb_color = colors.preto1,
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

        StateApp.register_callback('atualization_switch', self.alterar_switch)

    def _text(self, text : str, tamanho : int):
        return ft.Text(
            value = text,
            size = tamanho
        )
    
    def _mudou_valor_switch(self, e):
        self.switch.value = e.control.value
        self.update()

        StateApp.notify(event = "overlay_tips", data = e.control.value)
        StateApp.notify(event = "atualization_on_click", data = e.control.value)
    
    def alterar_switch(self, value):
        self.switch.value = value
        self.update()