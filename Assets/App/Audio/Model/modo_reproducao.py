from .musica import Musica
from enum import Enum

class ModoReprodução(Enum):
    PLAYLIST = 'playlist'
    FAVORITA = 'favorita'
    ARTISTA = 'artista'
    ALBUM = 'album'
    SEM_REPRODUCAO = 'sem_repdroducao'


class Reprodução:
    _listas_modos_reproduções : dict[ModoReprodução, list] = {
        ModoReprodução.PLAYLIST : [],
        ModoReprodução.FAVORITA : [],
        ModoReprodução.ARTISTA : [],
        ModoReprodução.ALBUM : []
    }
    _reproducao_atual : ModoReprodução = ModoReprodução.SEM_REPRODUCAO

    @classmethod
    def definir_modo(cls, novo_modo : ModoReprodução):
        cls._reproducao_atual = novo_modo

    @classmethod
    def retornar_modo(cls) -> ModoReprodução:
        return cls._reproducao_atual
    
    @classmethod
    def carregar_musicas_do_modo(cls, modo : ModoReprodução, lista : list[Musica]):
        if not lista:
            return
        
        cls._listas_modos_reproduções[modo].clear()
        cls._listas_modos_reproduções[modo].extend(lista)

    @classmethod
    def retornar_musicas_do_modo(cls):
        if cls._reproducao_atual != ModoReprodução.SEM_REPRODUCAO:
            return cls._listas_modos_reproduções[cls._reproducao_atual]
        

    # FUNÇÕES APENAS PARA AS FAVORITAS
    @classmethod
    def adicionar_musica(cls, musica):
        print(musica)

        if musica not in cls._listas_modos_reproduções[ModoReprodução.FAVORITA]:
            cls._listas_modos_reproduções[ModoReprodução.FAVORITA].append(musica)
            print(cls._listas_modos_reproduções[ModoReprodução.FAVORITA])

    @classmethod
    def remover_musica(cls, musica):
        for musica_favoritada in cls._listas_modos_reproduções[ModoReprodução.FAVORITA]:
            if musica_favoritada.chave == musica.chave:
                cls._listas_modos_reproduções[ModoReprodução.FAVORITA].remove(musica_favoritada)
                break