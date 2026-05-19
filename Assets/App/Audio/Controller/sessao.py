from ..Model.modelos import EstadoPlayer, ConfiguracaoReproducao
from ..Fontes.fonte_reproducao import FonteReproducao
from ..Model.reprodutor import Reprodutor

class SessaoReproducao:
    estado = EstadoPlayer()
    config = ConfiguracaoReproducao()

    fonte_atual : FonteReproducao = None

    fila : list = []
    indice_atual : int = 0

    _callbacks = {
        'tempo_total' : [],
        'tempo_atual' : [],
        'nome_musica' : [], # callback para att o player inferior com o nome.
        'nome_artista' : [], # callback para att o player inferior com o artista.
        'posicao_slider' : [],
        'musica_atual' : [] # callback para marcar musica que estiver tocando no momento.
    }

    # CALLBACKS
    @classmethod
    def registrar_callback(cls, evento : str, callback : callable):
        cls._callbacks[evento].append(callback)

    @classmethod
    def _notificar(cls, evento : str):
        for callback in cls._callbacks.get(evento, []):
            callback(cls)

    
    # FONTE
    @classmethod
    def definir_fonte(cls, fonte : FonteReproducao):
        cls.fonte_atual = fonte
        cls.fila = fonte.carregar()
        cls.indice_atual = 0
        cls._notificar('fila')


    # MÚSICA
    @classmethod
    def tocar_indice(cls, indice : int):
        if not cls.fila:
            return
        
        cls.indice_atual = indice

        musica = cls.fila[indice]

        cls.estado.musica_atual = musica
        cls.estado.tempo_atual = 0

        Reprodutor.carregar(musica.caminho)
        Reprodutor.tocar()

        cls.estado.tocando = True

        cls._notificar('musica_alterada')
        cls._notificar('musica_alterada')

    @classmethod
    def tocar_musica(cls, musica):
        for indice, m in enumerate(cls.fila):
            if m.id == musica.id:
                cls.tocar_indice(indice)
                break

    
    # CONTROLES
    @classmethod
    def toggle_play(cls):
        cls.estado.tocando = not cls.estado.tocando

        if cls.estado.tocando:
            Reprodutor.tocar()
        else:
            Reprodutor.pausar()

        cls._notificar('')
    
    @classmethod
    def proxima(cls):
        if not cls.fila:
            return
        
        cls.indice_atual += 1

        if cls.indice_atual >= len(cls.fila):
            cls.indice_atual = 0

        cls.tocar_indice(cls.indice_atual)

    @classmethod
    def anterior(cls):
        if not cls.fila:
            return
        
        cls.indice_atual -= 1

        if cls.indice_atual < 0:
            cls.indice_atual = len(cls.fila) - 1

        cls.tocar_indice(cls.indice_atual)

    
    # CONFIGURAÇÕES
    @classmethod
    def toggle_aleatorio(cls):
        cls.config.aleatorio = not cls.config.aleatorio

    @classmethod
    def toggle_repetir(cls):
        cls.config.repetir = not cls.config.repetir

    
    # TEMPO
    @classmethod
    def atualizar_tempo(cls, tempo : float):
        cls.estado.tempo_atual = tempo
        cls._notificar('')
    
    @classmethod
    def definir_volume(cls, volume : float):
        cls.estado.volume = volume
        cls._notificar('')