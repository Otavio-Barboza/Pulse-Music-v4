from .detector_idioma import detectar_idioma
from deep_translator import GoogleTranslator

class Tradutor(GoogleTranslator):
    def __init__(
        self, 
        source = "auto", 
        target = "en", 
        proxies = None, 
        **kwargs
    ):
        super().__init__(source, target, proxies, **kwargs)