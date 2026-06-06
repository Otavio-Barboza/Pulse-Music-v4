from ..Model.modelos import EstadoPlayer, ConfiguracaoReproducao
from ..Model.modo_reproducao import Reprodução
from ..Model.reprodutor import Reprodutor
from ...Playlists.Controller.estado_playlist import EstadoPlay
from ...Letras.Controller.letras_services import LetrasServices

class SessaoReproducao:
    estado = EstadoPlayer()
    config = ConfiguracaoReproducao()

    fonte_atual : Reprodução = Reprodução._reproducao_atual

    fila : list = []
    fila_aleatoria : list = []
    indice_atual : int = 0

    _monitor_iniciado = False
    _slider_arrastando = False

    _callbacks = {
        'volume' : [],
        'tempo_total' : [],
        'posicao_slider' : [],
        'musica_atual' : [], # callback para marcar musica que estiver tocando no momento.
        'slider' : [],
        'att_container' : [],
        'play/pause' : [],
        'repetir' : [],
        'aleatorio' : []
    }

    LetrasServices.registrar_callback(
        evento = 'buscar_letra',
        callback = LetrasServices.buscar_letra
    )

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
    def definir_fonte(cls):
        import random

        cls.fonte_atual = Reprodução.retornar_modo()
        cls.fila = Reprodução.retornar_musicas_do_modo()[:]
        cls.fila_aleatoria = cls.fila[:]
        random.shuffle(cls.fila_aleatoria)
        cls.indice_atual = 0

    @classmethod
    def atualizar_filas(cls):
        from ...Audio.Model.modo_reproducao import ModoReprodução
        import random
        
        if (
            cls.fila is None
             or 
            cls.fonte_atual != ModoReprodução.FAVORITA
        ):
            return
                
        cls.fila.clear()
        cls.fila.extend(Reprodução.retornar_musicas_do_modo())

        cls.fila_aleatoria.clear()
        cls.fila_aleatoria.extend(cls.fila[:])
        random.shuffle(cls.fila_aleatoria)

    @classmethod
    def atualizar_filas_scanner(cls, *_):
        cls.fila.clear()
        cls.fila.extend(
            Reprodução.retornar_musicas_do_modo()[:]
        )

        cls.fila_aleatoria.clear()
        cls.fila_aleatoria.extend(cls.fila[:])
        
        if cls.estado.musica_atual is None:
            return

        for i, musica in enumerate(cls.fila):
            if musica.chave == cls.estado.musica_atual.chave:
                cls.indice_atual = i
                return
    

    # MÚSICA
    @classmethod
    def receber_indice(cls, chave : str):
        for indice, musica in enumerate(cls.fila):
            if musica.chave == chave:
                cls.indice_atual = indice
                break

    @classmethod
    def tocar_indice(cls):
        cls.estado.tempo_atual = 0

        if not cls._monitor_iniciado:
            cls.iniciar_monitor_tempo()
            cls._monitor_iniciado = True

        if not cls.fila:
            return
        
        musica = cls.fila[cls.indice_atual] if not cls.config.aleatorio else cls.fila_aleatoria[cls.indice_atual]

        cls.estado.musica_atual = musica
        cls.estado.tempo_atual = 0

        Reprodutor.carregar(musica.caminho)
        Reprodutor.tocar()

        cls.definir_status_tocando(True)

        cls._notificar('att_container')
        cls._notificar('play/pause')
        cls._notificar('musica_atual')
        
        LetrasServices._notificar(
            evento = 'buscar_letra',
            dados = {
                'chave' : cls.estado.musica_atual.chave,
                'nome' : cls.buscar_nome(),
                'artista' : cls.buscar_artista()
            }
        )

        if LetrasServices._tela_expandida:
            LetrasServices._notificar(
                evento = 'att_letra',
                dados = None
            )

    @classmethod
    def definir_status_tocando(cls, valor : bool):
        cls.estado.tocando = valor


    # CONTROLES
    @classmethod
    def toggle_play_pause(cls):
        cls.definir_status_tocando(not cls.estado.tocando)

        if cls.estado.tocando:
            Reprodutor.tocar()
        else:
            Reprodutor.pausar()

        cls._notificar('play/pause')
    
    @classmethod
    def proxima(cls):
        if not cls.fila:
            return
        
        cls.indice_atual += 1

        if cls.indice_atual >= len(cls.fila):
            cls.indice_atual = 0

        cls.tocar_indice()

    @classmethod
    def anterior(cls):
        if not cls.fila:
            return
        
        cls.indice_atual -= 1

        if cls.indice_atual < 0:
            cls.indice_atual = len(cls.fila) - 1

        cls.tocar_indice()

    
    # CONFIGURAÇÕES
    @classmethod
    def toggle_aleatorio(cls):
        cls.config.aleatorio = not cls.config.aleatorio
        cls._notificar('aleatorio')

    @classmethod
    def toggle_repetir(cls):
        cls.config.repetir = not cls.config.repetir
        cls._notificar('repetir')

    
    # MONITOR
    @classmethod
    def definir_arrasto_slider(cls, valor : bool):
        cls._slider_arrastando = valor
        
    @classmethod
    def inicar(cls):
        if cls._monitor_iniciado:
            return
        
        cls._monitor_iniciado = True
        cls.iniciar_monitor_tempo()

    @classmethod
    def iniciar_monitor_tempo(cls):
        import threading

        def loop():
            import time

            while True:
                if (
                    cls.estado.tocando 
                     and 
                    not cls._slider_arrastando
                ):
                    duracao_pura = Reprodutor.duracao_pura()

                    if (
                        cls.estado.duracao_total != duracao_pura
                         or
                        duracao_pura == 0.0
                    ):
                        cls.atualizar_tempo_total()
                        cls._notificar('slider')

                    tempo = Reprodutor.posicao_pura()
                    cls.atualizar_tempo(tempo)

                time.sleep(0.2)
        
        threading.Thread(
            target = loop,
            daemon = True
        ).start()


    # TEMPO
    @classmethod
    def atualizar_tempo(cls, tempo : float):
        cls.estado.tempo_atual = tempo
        cls._notificar('posicao_slider')

    @classmethod
    def atualizar_tempo_total(cls):
        cls.estado.duracao_total = Reprodutor.duracao_pura()
        cls._notificar('tempo_total')

    @classmethod
    def formatar_tempo_atual(cls):
        minutos = int(SessaoReproducao.estado.tempo_atual / 60)
        segundos = int(SessaoReproducao.estado.tempo_atual - (minutos * 60))
        return f'{minutos:02}:{segundos:02}' or '00:00'
    
    @classmethod
    def formatar_tempo_total(cls):
        minutos = int(SessaoReproducao.estado.duracao_total / 60)
        segundos = int(SessaoReproducao.estado.duracao_total - (minutos * 60))
        return f'{minutos:02}:{segundos:02}' or '00:00'

    @classmethod
    def ir_para(cls, valor : float):
        Reprodutor.ir_para(valor)
        cls._notificar('posicao_slider')


    # VOLUME
    @classmethod
    def definir_volume(cls, volume : float):
        cls.estado.volume = volume
        Reprodutor.set_volume(cls.estado.volume)
        cls._notificar('volume')

    
    # TRATAMENTO AUTOMÁTICO DA MÚSICA
    @classmethod
    def tratar_fim_da_musica(cls):
        if cls.config.repetir:
            cls.tocar_indice()
        else:
            cls.proxima()
            
    
    # OUTROS
    @classmethod
    def buscar_artista(cls) -> str:
        from ..Repository.musica_repositorio import RepositorioMusica
        return RepositorioMusica.buscar_artista(cls.estado.musica_atual.chave)
    
    @classmethod
    def buscar_nome(cls) -> str:
        from ..Repository.musica_repositorio import RepositorioMusica
        return RepositorioMusica.buscar_musica(cls.estado.musica_atual.chave)

    @classmethod
    def buscar_capa(cls) -> str:
        from ..Repository.musica_repositorio import RepositorioMusica
        return RepositorioMusica.buscar_capa(cls.estado.musica_atual.nome)