# imports de back-end
from core.lyrics.model.genius import Genius
from core.lyrics.translate.translator import Translator
from core.lyrics.cache.cache_lyrics import CacheLyrics
from core.lyrics.translate.language_detect import language_detect
from core.services.account_manager import AccountManager
from core.utils.utils import Utils
from core.utils.path import AppPaths

# import geral
from deep_translator.exceptions import TranslationNotFound
import requests, time


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
    def register_callback(cls, event: str, callback: callable):
        if event not in cls.callbacks:
            cls.callbacks[event] = []
        cls.callbacks[event].append(callback)

    @classmethod
    def notify(cls, data, event: str):
        for callback in cls.callbacks.get(event, []):
            callback(data)

    @classmethod
    def set_expanded_screen(cls, valor: bool):
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
                cls.notify(
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
            (cls.translator.source is None)
            or (cls.translator.target is None)
        ):
            return

        for attempt in range(5):
            try:
                return cls.translator.translate(lyric)
            except TranslationNotFound:
                if attempt < 4:
                    time.sleep(0.5)
        else:
            return None
        
    @classmethod
    def save_lyric(cls, lyric: str, key_song: str, original_lyric: str):
        existing_letters = Utils.sync_load_json(
            AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "lyrics.json"
        )

        existing_letters[key_song] = {
            "original_lyric" : lyric,
            "original_language" : original_lyric,
            "translations" : []
        }

        Utils.sync_update_json(
            data = existing_letters, 
            path =  AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "lyrics.json"
        )

    @classmethod
    def update_translations(cls, key_song: str, new_language: str, new_lyric: str):
        existing_letters = Utils.sync_load_json(
            AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "lyrics.json"
        )

        if not any(
            translation["language"] == new_language
            for translation in existing_letters[key_song]["translations"]
        ):
            existing_letters[key_song]["translations"].append({
                "language" : new_language,
                "lyric" : new_lyric
            })
        
        Utils.sync_update_json(
            data = existing_letters, 
            path = AppPaths.ACCOUNT / AccountManager.accounts_cache.get("current_account") / "music" / "lyrics.json"
        )

    @classmethod
    def start_translation(cls, language: str):
        from core.song.controller.reproduction_manager import ReproductionManager

        # Senão tiver nenhuma música definida, não tem nada para traduzir
        if ReproductionManager.state.current_song is None:
            return "Nenhuma lyric carregada para tradução"


        # Tenta buscar a letra com base na linguagem definida.
        existing_translated_lyric = CacheLyrics.return_translated_lyric(language)

        # Se existir a letra, retorna ela.
        if existing_translated_lyric is not None:
            return existing_translated_lyric


        # Parte 2

        # pega a letra original
        lyric = CacheLyrics.return_lyric()

        # Senão houver diz que não encontrou
        if not lyric:
            return "A letra musical não foi encontrada. Portanto, não é possível traduzir!"


        # traduz a letra
        translated_lyric = cls.translate(lyric)

        # se der erro na tradução, retorna que não foi possível
        if not translated_lyric:
            return "Falha na tradução, tente novamente!"


        # Atualiza o json com as letras
        cls.update_translations(
            key_song = ReproductionManager.state.current_song.key,
            new_language = language,
            new_lyric = translated_lyric
        )


        # atualiza o cache
        CacheLyrics.load_cache()


        # retorna a letra traduzida
        return translated_lyric