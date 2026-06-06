class LetrasMemoria:
    _letras = {}

    @classmethod
    def carregar_memoria(cls):
        from ..Repository.letra_repository import LetraRepository
        cls._letras = LetraRepository.ler_json()

    @classmethod
    def retornar_letra(cls) -> str:
        from ...Audio.Controller.sessao import SessaoReproducao
        
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
    def retornar_letra_traduzida(cls, idioma : str) -> str:
        from ...Audio.Controller.sessao import SessaoReproducao
        
        if SessaoReproducao.estado.musica_atual is None:
            return None
        
        if SessaoReproducao.estado.musica_atual.chave not in cls._letras:
            return None
        
        letras = cls._letras[
            SessaoReproducao.estado.musica_atual.chave
        ].get('traducoes')

        if len(letras) == 0:
            return None
        
        for traducao in letras:
            if traducao.get('idioma') == idioma:
                return traducao.get('letra')
        else:
            return None