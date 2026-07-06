from difflib import SequenceMatcher

class Validacao:
    @classmethod
    def similaridade(cls, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()