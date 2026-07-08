# imports de back-end
from project.core.song.model.data_song import PlayerState, ReproductionConfiguration
from project.core.song.model.reproduction import Reproduction
from project.core.song.model.player import Player
from project.core.song.enum.song_enum import ReproductionMode
from ...Letras.Controller.letras_services import LetrasServices
from project.core.song.model.song import Song
from project.core.song.repository.song_repository import SongRepository

# import geral
import random, threading, time


class ReproductionManager:

    state = PlayerState()
    configuration = ReproductionConfiguration()

    current_font: ReproductionMode = Reproduction._current_reproduction

    _queue: list[Song] = []
    _random_queue: list[Song] = []
    _current_index: int = 0

    _is_monitoring: bool = False
    _slider_dragging: bool = False

    _callbacks: dict[str, list] = {
        'volume' : [],
        'tempo_total' : [],
        'slider_position' : [],
        'musica_atual' : [], # callback para marcar musica que estiver tocando no momento.
        'slider' : [],
        'att_container' : [],
        'play/pause' : [],
        'repeat' : [],
        'aleatorio' : []
    }

    LetrasServices.registrar_callback(
        evento = 'buscar_letra',
        callback = LetrasServices.buscar_letra
    )

    # CALLBACKS
    @classmethod
    def register_callback(cls, event: str, callback: callable):
        cls._callbacks[event].append(callback)

    @classmethod
    def notify(cls, event: str):
        for callback in cls._callbacks.get(event, []):
            callback(cls)

    
    # FONTE
    @classmethod
    def set_font(cls):
        cls.current_font = Reproduction.return_current_reproduction()
        
        cls._queue = Reproduction.return_songs_for_mode()[:]
        cls._random_queue = cls._queue[:]
        random.shuffle(cls._random_queue)

        cls._current_index = 0

    @classmethod
    def update_queues(cls):        
        if (
            cls._queue is None
            or cls.current_font != ReproductionMode.FAVORITE
        ):
            return
                
        cls._queue.clear()
        cls._queue.extend(Reproduction.return_songs_for_mode())

        cls._random_queue.clear()
        cls._random_queue.extend(cls._queue[:])
        random.shuffle(cls._random_queue)

    @classmethod
    def update_queue_scanner(cls, *_):
        cls._queue.clear()
        cls._queue.extend(
            Reproduction.return_songs_for_mode()[:]
        )

        cls._random_queue.clear()
        cls._random_queue.extend(cls._queue[:])
        
        if cls.state.current_song is None:
            return

        index: int
        song: Song

        for index, song in enumerate(cls._queue):
            if song.key == cls.state.current_song.key:
                cls._current_index = index
                return
    

    # MÚSICA
    @classmethod
    def get_index(cls, key: str):
        index: int
        song: Song

        for index, song in enumerate(cls._queue):
            if song.key == key:
                cls._current_index = index
                break

    @classmethod
    def play(cls):
        cls.state.current_time = 0

        if not cls._is_monitoring:
            cls.start_time_monitor()
            cls._is_monitoring = True

        if not cls._queue:
            return
        
        song: Song = cls._queue[cls._current_index] if not cls.configuration.shuffle else cls._random_queue[cls._current_index]

        cls.state.current_song = song
        cls.state.current_time = 0

        Player.load_song(song.path)
        Player.play()

        cls.set_is_playing(True)

        cls.notify('actualization_container')
        cls.notify('play/pause')
        cls.notify('current_song')
        
        LetrasServices.notify(
            evento = 'buscar_letra',
            dados = {
                'chave' : cls.state.current_song.chave,
                'nome' : cls.buscar_nome(),
                'artista' : cls.buscar_artista()
            }
        )

        if LetrasServices._tela_expandida:
            LetrasServices.notify(
                evento = 'att_letra',
                dados = None
            )

    @classmethod
    def set_is_playing(cls, value: bool):
        cls.state.is_playing = value


    # CONTROLES
    @classmethod
    def toggle_play_pause(cls):
        cls.set_is_playing(not cls.state.is_playing)

        if cls.state.is_playing:
            Player.play()
        else:
            Player.pause()

        cls.notify('play/pause')
    
    @classmethod
    def next(cls):
        if not cls._queue:
            return
        
        cls._current_index += 1

        if cls._current_index >= len(cls._queue):
            cls._current_index = 0

        cls.play()

    @classmethod
    def previous(cls):
        if not cls._queue:
            return
        
        cls._current_index -= 1

        if cls._current_index < 0:
            cls._current_index = len(cls._queue) - 1

        cls.play()

    
    # CONFIGURAÇÕES
    @classmethod
    def toggle_shuffle(cls):
        cls.configuration.shuffle = not cls.configuration.shuffle
        cls.notify('shuffle')

    @classmethod
    def toggle_repeat(cls):
        cls.configuration.repeat = not cls.configuration.repeat
        cls.notify('repeat')

    
    # MONITOR
    @classmethod
    def set_drag_slider(cls, value: bool):
        cls._slider_dragging = value
        
    @classmethod
    def start(cls):
        if cls._is_monitoring:
            return
        
        cls._is_monitoring = True
        cls.start_time_monitor()

    @classmethod
    def start_time_monitor(cls):

        def loop():

            while True:
                if (
                    cls.state.is_playing 
                    and not cls._slider_dragging
                ):
                    current_duration = Player.current_duration()

                    if (
                        cls.state.total_time != current_duration
                        or current_duration == 0.0
                    ):
                        cls.update_total_time()
                        cls.notify('slider')

                    tempo = Player.current_position()
                    cls.update_time(tempo)

                time.sleep(0.2)
        
        threading.Thread(
            target = loop,
            daemon = True
        ).start()


    # TEMPO
    @classmethod
    def update_time(cls, time: float):
        cls.state.current_time = time
        cls.notify('slider_position')

    @classmethod
    def update_total_time(cls):
        cls.state.total_time = Player.current_duration()
        cls.notify('total_time')

    @classmethod
    def formatted_current_duration(cls) -> str:
        return Player.formatted_current_duration()
    
    @classmethod
    def formatted_total_duration(cls) -> str:
        return Player.formatted_total_duration()

    @classmethod
    def go_to(cls, value: float):
        Player.go_to(value)
        cls.notify('slider_position')


    # VOLUME
    @classmethod
    def set_volume(cls, volume: float):
        cls.state.volume = volume
        Player.set_volume(cls.state.volume)
        cls.notify('volume')

    
    # TRATAMENTO AUTOMÁTICO DA MÚSICA
    @classmethod
    def handle_end_of_music(cls):
        if cls.configuration.repeat:
            cls.play()
        else:
            cls.next()
            
    
    # OUTROS
    @classmethod
    def buscar_artista(cls) -> str:
        return SongRepository.get_artist(cls.state.current_song.key)
    
    @classmethod
    def buscar_nome(cls) -> str:
        return SongRepository.get_song(cls.state.current_song.key)

    @classmethod
    def buscar_capa(cls) -> str:
        return SongRepository.get_cover(cls.state.current_song.name)