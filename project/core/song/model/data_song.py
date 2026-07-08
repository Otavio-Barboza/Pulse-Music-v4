# import de back-end
from project.core.song.model.song import Song

# import geral
from dataclasses import dataclass


# dataclass para armazenar dados nas classes, operação semelhante ao usar a classe com def __init__(self).
@dataclass
class PlayerState:

    current_song: Song = None
    is_playing: bool = False
    current_time: float = 0.0
    total_time: float = 0.0
    volume: float = 1.0


# dataclass para armazenar dados nas classes, operação semelhante ao usar a classe com def __init__(self).
@dataclass
class ReproductionConfiguration:

    shuffle: bool = False
    repeat: bool = False