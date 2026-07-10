class LyricsMemory:
    _letras = {}
    cache_lyrics = None

    @classmethod
    def load_memory(cls):
        from ..Repository.letra_repository import LetraRepository
        cls._letras = LetraRepository.ler_json()

    @classmethod
    def return_lyrics(cls) -> str:
        from ...Audio.Controller.sessao import SessionReproduction
        
        if SessaoReproducao.estado.musica_atual is None:
            return 'Letra não Encontrada'
        
        if SessaoReproducao.estado.musica_atual.chave not in cls._letras:
            return 'Letra não Encontrada'
        
        letra = cls._letras[
            SessaoReproducao.estado.musica_atual.chave
        ].get('letra_original')

        if letra is None:
            return 'Letra não encontrata'
        return letra
    
    @classmethod
    def return_translated_lyrics(cls, language: str) -> str:
        from ...Audio.Controller.sessao import SessaoReproducao
        
        if SessaoReproducao.estado.musica_atual is None:
            return None
        
        if SessaoReproducao.estado.musica_atual.chave not in cls._letras:
            return None
        
        lyrics = cls._letras[
            SessaoReproducao.estado.musica_atual.chave
        ].get('traducoes')

        if len(lyrics) == 0:
            return None
        
        for traducao in lyrics:
            if traducao.get('language') == language:
                return traducao.get('letra')
        else:
            return None
        
    @classmethod
    def update_cache(cls, language):
        cls.cache_lyrics = language