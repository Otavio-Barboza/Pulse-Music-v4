# imports de back-end
from core.lyrics.model.genius import Genius
from core.lyrics.translate.translator import Translator
from core.lyrics.cache.cache_lyrics import CacheLyrics
from core.lyrics.translate.language_detect import language_detect
from core.utils.utils import Utils

# import geral
import requests


class LyricsServices:

    expanded_screen: bool = False
    GENIUS = Genius()
    translator = Translator()

    AVAILABLE_LANGUAGES : dict[str, str] = {}    
    for language, uf in translator._languages.items():
        AVAILABLE_LANGUAGES[
            language.replace(" ", "_")
        ] = uf

    callbacks = {}

    @classmethod
    def register_callback(cls, event: str, callback : callable):
        if event not in cls.callbacks:
            cls.callbacks[event] = []
        cls.callbacks[event].append(callback)

    @classmethod
    def notify(cls, data, event : str):
        for callback in cls.callbacks.get(event, []):
            callback(data)

    @classmethod
    def set_expanded_screen(cls, valor : bool):
        cls.expanded_screen = valor

    @classmethod
    def get_lyric(cls, data: dict) -> str | None:
        try:    
            if data.get("key") in CacheLyrics.lyric:
                return
            
            song = cls.GENIUS.search_song(
                title = data.get("name"),
                artist = data.get("artist")
            )
            
            if not song:
                return
            
            cls.save_lyric(
                key_song = data.get("key"),
                lyric = song.lyrics,
                original_lyric = language_detect(song.lyrics)
            )

            CacheLyrics.load_cache()

            if cls.expanded_screen:
                cls.notifify(
                    event = "actualization_lyric",
                    data = None
                )

        except requests.exceptions.Timeout:
            print("Timeout ao buscar lyric.")
            return
        except Exception as erro:
            print(f"Erro: {erro}")
            return 
    
    @classmethod
    def set_language_target(cls, target: str):
        cls.translator.target = target

    @classmethod
    def translate(cls, lyric: str) -> str | None:
        cls.translator.source = language_detect(lyric)
        
        if (
            cls.translator.source is None
             or
            cls.translator.target is None
        ):
            return
        return cls.translator.translate(lyric)
    
    @classmethod
    def save_lyric(cls, lyric: str, key_song: str, original_lyric: str):
        existing_letters = Utils.sync_load_json()

        existing_letters[key_song] = {
            "original_lyric" : lyric,
            "original_language" : original_lyric,
            "translations" : []
        }

        Utils.sync_update_json(data = existing_letters, path = None)

    @classmethod
    def update_translations(cls, key_song: str, new_language: str, new_lyric: str):
        existing_letters = Utils.sync_load_json()

        if new_language not in existing_letters[key_song]["translations"]:
            existing_letters[key_song]["translations"].append({
                "language" : new_language,
                "lyric" : new_lyric
            })

        Utils.sync_update_json(data = existing_letters, path = None)

    @classmethod
    def start_translation(cls, language: str):
        from core.song.controller.reproduction_manager import ReproductionManager

        if ReproductionManager.state.current_song is None:
            return "Nenhuma lyric carregada para tradução"
        
        existing_translated_lyrics = CacheLyrics.return_translated_lyric(language)
        
        if existing_translated_lyrics is not None:
            return existing_translated_lyrics
        
        lyric = CacheLyrics.return_lyric()

        if not lyric:
            return "A respectiva lyric não foi encontrada. Portanto, não é possível translate!"
        
        translated_lyric = cls.translate(lyric)

        if not translated_lyric:
            return "Falha na tradução, tente novamente!"
        
        cls.update_translations(
            key_song = ReproductionManager.state.current_song.key,
            new_language = language,
            new_lyric = translated_lyric
        )

        CacheLyrics.load_cache()

        return translated_lyric