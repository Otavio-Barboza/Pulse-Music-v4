from ...Audio.Model.musica import Musica
from ..Repository.favorita_repository import FavoritasRepository
from enum import Enum

class Favoritada(Enum):
    FAVORITADA = 'favoritada'
    NAO_FAVORITADA = 'não-favoritada'


class EstadoFavoritas:
    _callbacks : dict[str, list] = {}
    # lista com objetos Musica
    _lista_favoritas : list[Musica] = []

    @classmethod
    def registrar_callback(cls, evento : str, callback : callable):
        if evento not in cls._callbacks:
            cls._callbacks[evento] = []
        cls._callbacks[evento].append(callback)

    @classmethod
    def notificar(cls, evento : str, dados = None):
        import inspect, asyncio

        if evento not in cls._callbacks:
            return
        
        for func in cls._callbacks[evento]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(dados))
                else:
                    res = func(dados)
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                import traceback
                print(f"[CALLBACK ERROR]: {e}")
                traceback.print_exc()

    @classmethod
    def listar_objetos_favoritados(cls) -> list[Musica]:
        return FavoritasRepository.listar_objetos_favoritados()
    
    @classmethod
    def alterar_objeto_para_json(cls, dados : Musica):
        nova_chave, novo_item = FavoritasRepository.formatar_objeto_no_json(
            dado = dados, 
            status = Favoritada.FAVORITADA.value
        )

        json_musicas = FavoritasRepository.ler_json()

        if nova_chave not in json_musicas:
            json_musicas[nova_chave] = novo_item

        FavoritasRepository.salvar_json(json_musicas)

        dados.modo = Favoritada.FAVORITADA.value

        cls.notificar(
            evento = 'favoritar',
            dados = dados
        )

    @classmethod
    def remover_favorita_json(cls, dado : Musica):
        json_favorita = FavoritasRepository.ler_json()
        chave_para_remover = None

        for chave, _ in json_favorita.items():
            if chave == dado.chave:
                chave_para_remover = chave
                break
        
        if chave_para_remover is None:
            return 
        
        del json_favorita[chave_para_remover]
        FavoritasRepository.salvar_json(json_favorita)

        cls.notificar(
            'desfavoritar',
            dado
        )  
        
    @classmethod
    def listar_favoritas(cls) -> list[str]:
        return FavoritasRepository.listar_favoritas()
    
    @classmethod
    def adicionar_musica_reproducao(cls, musica : Musica):
        from ...Audio.Model.modo_reproducao import Reprodução
        Reprodução.adicionar_musica(musica)

    @classmethod
    def remover_musica_reproducao(cls, musica : Musica):
        from ...Audio.Model.modo_reproducao import Reprodução
        Reprodução.remover_musica(musica)