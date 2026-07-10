# import geral
from deep_translator import GoogleTranslator


class Translator(GoogleTranslator):
    def __init__(
        self, 
        source = "auto", 
        target = "en", 
        proxies = None, 
        **kwargs
    ):
        super().__init__(source, target, proxies, **kwargs)