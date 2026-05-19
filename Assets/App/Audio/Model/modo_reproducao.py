from enum import Enum

class ModoReprodução(Enum):
    PLAYLIST = 'playlist'
    FAVORITA = 'favorita'
    ARTISTA = 'artista'
    ALBUM = 'album'
    SEM_REPRODUCAO = 'sem_repdroducao'

class Reprodução:
    _reproducao_atual = ModoReprodução.SEM_REPRODUCAO

    @classmethod
    def definir_modo(cls, novo_modo : ModoReprodução):
        cls.reproducao_atual = novo_modo

    @classmethod
    def retornar_modo(cls) -> ModoReprodução:
        return cls.reproducao_atual