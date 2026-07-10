# imports de back-end
from project.core.lyrics.model.genius import Genius
from ..Repository.letra_repository import LetraRepository
from ..Translate.tradutor import Tradutor

# import geral
import requests


class LyricsServices:
    _expanded_screen = False
    GENIUS = Genius()
    TRADUTOR = Tradutor()

    _LINGUAGENS_DIPONIVEIS : dict[str, str] = {}    
    for language, uf in TRADUTOR._languages.items():
        _LINGUAGENS_DIPONIVEIS[
            language.replace(' ', '_')
        ] = uf

    _callbacks = {}

    @classmethod
    def register_callback(cls, event: str, callback : callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(callback)

    @classmethod
    def notifify(cls, data, event : str):
        for callback in cls._callbacks.get(event, []):
            callback(data)

    @classmethod
    def set_expanded_screen(cls, valor : bool):
        cls._expanded_screen = valor

    @classmethod
    def get_lyric(cls, data: dict) -> str | None:
        from ..Translate.detector_idioma import detectar_idioma
        from ..Cache.memoria_letras import LetrasMemoria

        try:    
            if data.get('key') in LetrasMemoria._letras:
                return
            
            song = cls.GENIUS.search_song(
                title = data.get('nome'),
                artist = data.get('artista')
            )
            
            if not song:
                return
            
            cls.save_lyric(
                key_song = data.get('chave'),
                lyric = song.lyrics,
                idioma_padrao = detectar_idioma(song.lyrics)
            )

            LetrasMemoria.carregar_memoria()

            if cls._expanded_screen:
                cls._notificar(
                    evento = 'att_letra',
                    data = None
                )

        except requests.exceptions.Timeout:
            print("Timeout ao buscar lyric.")
            return
        except Exception as erro:
            print(f"Erro: {erro}")
            return 
    
    @classmethod
    def set_language_target(cls, saida : str):
        cls.TRADUTOR.target = saida

    @classmethod
    def translate(cls, lyric : str) -> str | None:
        from Assets.App.Letras.Translate.detector_idioma import detectar_idioma

        cls.TRADUTOR.source = detectar_idioma(lyric)
        
        if (
            cls.TRADUTOR.source is None
             or
            cls.TRADUTOR.target is None
        ):
            return
        return cls.TRADUTOR.translate(lyric)
    
    @classmethod
    def save_lyric(cls, lyric, key_song, idioma_padrao):
        letras_existentes = LetraRepository.ler_json()

        letras_existentes[key_song] = {
            'letra_original' : lyric,
            'idioma_original' : idioma_padrao,
            'translations' : []
        }

        LetraRepository.salvar_json(letras_existentes)

    @classmethod
    def update_translations(cls, key_song : str, new_language : str, new_lyric : str):
        letras_existentes = LetraRepository.ler_json()

        if new_language not in letras_existentes[key_song]['translations']:
            letras_existentes[key_song]['translations'].append({
                'language' : new_language,
                'lyric' : new_lyric
            })

        LetraRepository.salvar_json(letras_existentes)

    @classmethod
    def start_translation(cls, language : str):
        from ..Cache.memoria_letras import LetrasMemoria
        from ...Audio.Controller.sessao import SessaoReproducao

        if SessaoReproducao.estado.musica_atual is None:
            return 'Nenhuma lyric carregada para tradução'
        
        letra_traduzida_existente = LetrasMemoria.retornar_letra_traduzida(language)
        
        if letra_traduzida_existente is not None:
            return letra_traduzida_existente
        
        lyric = LetrasMemoria.retornar_letra()

        if not lyric:
            return 'A respectiva lyric não foi encontrada. Portanto, não é possível translate!'
        
        letra_traduzida = cls.translate(lyric)

        if not letra_traduzida:
            return 'Falha na tradução, tente novamente!'
        
        cls.update_translations(
            key_song = SessaoReproducao.estado.musica_atual.chave,
            new_language = language,
            new_lyric = letra_traduzida
        )

        LetrasMemoria.carregar_memoria()

        return letra_traduzida