# import de back-end
from project.core.utils.utils import Utils
from project.core.song.controller.reproduction_manager import ReproductionManager


class CacheLyrics:
    
    lyric = {}
    cache_lyrics = None

    @classmethod
    def load_cache(cls):
        cls.lyric = Utils.sync_load_json()

    @classmethod
    def return_lyric(cls) -> str:        
        if ReproductionManager.state.current_song is None:
            return 'Letra não Encontrada'
        
        if ReproductionManager.state.current_song.key not in cls.lyric:
            return 'Letra não Encontrada'
        
        lyric = cls.lyric[
            ReproductionManager.state.current_song.key
        ].get('original_lyric')

        if lyric is None:
            return 'Letra não encontrata'
        return lyric
    
    @classmethod
    def return_translated_lyric(cls, language: str) -> str:        
        if ReproductionManager.state.current_song is None:
            return None
        
        if ReproductionManager.state.current_song.key not in cls.lyric:
            return None
        
        lyrics = cls.lyric[
            ReproductionManager.state.current_song.key
        ].get('translations')

        if len(lyrics) == 0:
            return None
        
        translation: dict
        
        for translation in lyrics:
            if translation.get('language') == language:
                return translation.get('lyric')
        else:
            return None
        
    @classmethod
    def update_cache(cls, language: str):
        cls.cache_lyrics = language