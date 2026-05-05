from ...Audio.Model.reprodutor import Reprodutor
from ...Audio.Model.audio import AudioLoop
from ...Music.Repository.musica_repositorio import RepositorioMusica
from ...Music.Model.musica import Musica
from ...Music.Fontes.fonte_musica import FonteMusica
from ..Model.monitor import MonitorTempo
import threading

class EstadoMusica:
    fonte_atual : FonteMusica = None
    fila_normal = None
    fila_aleatoria = None
    fila_ativa = None
    indice_atual = None
    usuario_arrastando = False
    musica_atual = None
    tocando = False
    repetir = False
    aleatorio = False

    volume = 1.0
    
    tempo_atual = 0.0
    _tempo_atual_formatado = '00:00'
    duracao_total = 0.0
    _tempo_total_formatado = '00:00'

    historico = []
    TAMANHO_HISTORICO = 5

    _callbacks = {
        'play_state' : [],
        'musica_atual' : [],
        'duracao' : [],
        'progresso' : [],
        'volume' : [],
        'repetir' : [],
        'aleatorio' : [],
        'texto_barra_duracao' : [],
        'tempo' : [],
        'slider' : [],
        'att_container' : []
    }
    
    @classmethod
    def registrar_callback(cls, evento : str, callback):
        cls._callbacks[evento].append(callback)
    
    @classmethod
    def _notificar(cls, evento : str):
        for cb in cls._callbacks.get(evento, []):
            cb(cls)
    
    @classmethod
    def definir_fonte(cls, fonte : FonteMusica):
        cls.fonte_atual = fonte
        musicas = fonte.carregar()
        cls._criar_fila(musicas)
        cls._notificar('tempo')
     
    @classmethod
    def _criar_fila(cls, musicas):
        cls.fila_normal = list(musicas)
        cls.fila_aleatoria = []
        cls.fila_ativa = cls.fila_normal
        cls.indice_atual = 0
    
    @classmethod
    def _tocar_atual(cls):
        cls.musica_atual = cls.fila_ativa[cls.indice_atual]
        cls.historico.append(cls.musica_atual)
        cls.tempo_atual = 0
        cls.duracao_total = 0

        Reprodutor.carregar(cls.musica_atual.caminho)
        Reprodutor.tocar()
        cls.tocando = True

        if not hasattr(cls, '_monitor'):
            cls._monitor = MonitorTempo(cls)
            cls._monitor.start()
        
        cls.duracao_total = Reprodutor.duracao_pura()
        cls._tempo_total_formatado = Reprodutor.duracao()

        cls._notificar('musica_atual')
        cls._notificar('play_state')
        cls._notificar('texto_barra_duracao')
        cls._notificar(evento = 'att_container')
        
    @classmethod
    def definir_musica_atual(cls, musica):
        for i, m in enumerate(cls.fila_ativa):
            if m.id == musica.id:
                cls.indice_atual = i
                break

        cls._tocar_atual()

    @classmethod
    def toggle(cls):
        cls.tocando = not cls.tocando
        Reprodutor.tocar() if cls.tocando else Reprodutor.pausar()
        cls._notificar('play_state')

    @classmethod
    def toggle_repetir(cls):
        cls.repetir = not cls.repetir
        cls._notificar('repetir')

    @classmethod
    def toggle_aleatorio(cls):
        import random

        cls.aleatorio = not cls.aleatorio

        if cls.aleatorio:
            cls.recriar_fila_aleatorio()
            cls.fila_ativa = cls.fila_aleatoria
            cls.indice_atual = 0
        else:
            cls.redefinir_indice()
            cls.fila_ativa = cls.fila_normal

        cls._notificar('aleatorio')
    
    @classmethod
    def recriar_fila_aleatorio(cls):
        import random

        musicas = cls.fila_normal[:]
        recentes = set(cls.historico[-cls.TAMANHO_HISTORICO:])
        musicas = [m for m in musicas if m not in recentes]

        if not musicas:
            musicas = cls.fila_normal[:]
        
        random.shuffle(musicas)
        cls.fila_aleatoria = musicas

    @classmethod    
    def redefinir_indice(cls):
        for indice, musica in enumerate(cls.fila_normal):
            if musica.id == cls.musica_atual.id:
                cls.indice_atual = indice
                break

    @classmethod
    def pausar(cls):
        Reprodutor.pausar(musica = cls.musica_atual.nome)
    
    @classmethod
    def proxima(cls):        
        cls.indice_atual += 1

        if cls.indice_atual >= (len(cls.fila_ativa) - 1):
            cls.indice_atual = 0

        cls._tocar_atual()

    @classmethod
    def anterior(cls):
        if cls.indice_atual < 0:
            cls.indice_atual = len(cls.fila_ativa)
        cls.indice_atual -= 1

        cls._tocar_atual()

    @classmethod
    def modo_repetir(cls):
        cls._tocar_atual()
    
    @classmethod
    def tratar_fim_musica(cls):
        
        if cls.repetir:
            cls.modo_repetir()
            return
        
        cls.indice_atual += 1

        if cls.indice_atual >= len(cls.fila_ativa) - 1:
            cls.indice_atual = 0

            if cls.aleatorio:
                cls.recriar_fila_aleatorio()
                cls.fila_ativa = cls.fila_aleatoria

        cls._tocar_atual()
    
    @classmethod
    def definir_volume(cls, volume : float):
        cls.volume = volume
        print(cls.volume)
        Reprodutor.set_volume(volume = volume)
        cls._notificar('volume')
        
    @classmethod
    def definir_duracao_total(cls):
        cls.duracao_atual = Reprodutor.duracao()
    
    @classmethod
    def atualizar_tempo(cls, tempo : float):
        cls.tempo_atual = tempo
        cls._tempo_atual_formatado = Reprodutor.posicao()
        cls._notificar('tempo')
    
    @classmethod
    def definir_posicao(cls, nova_posicao):
        cls.tempo_atual = nova_posicao
    
    @classmethod
    def ir_para(cls, segundos : float):
        if not cls.musica_atual:
            return
        
        if segundos < 0:
            segundos = 0
        
        if segundos > cls.duracao_total:
            segundos = cls.duracao_total
        
        Reprodutor.ir_para(segundos)
        cls.tempo_atual = segundos

        cls._notificar('slider')