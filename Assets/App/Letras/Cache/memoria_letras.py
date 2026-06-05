class LetrasMemoria:
    _letras = {}

    @classmethod
    def carregar_memoria(cls):
        from ..Repository.letra_repository import LetraRepository
        cls._letras = LetraRepository.ler_json()

    @classmethod
    def retornar_letra(cls) -> str:
        from ...Audio.Controller.sessao import SessaoReproducao
        
        letra = cls._letras[
            SessaoReproducao.estado.musica_atual.chave
        ].get('letra_original')

        if letra is None:
            return 'Letra não encontrata'
        return letra