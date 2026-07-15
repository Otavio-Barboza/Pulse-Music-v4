# imports gerais
from pathlib import Path
from flet import Colors


class PlaylistCard:
    def __init__(
        self, 
        id: str, 
        name: str, 
        image_path: Path, 
        color: Colors, 
        opacity: float, 
        playlist_path: Path,
        number_of_songs: int
    ):
        self.id = id
        self.name = name
        self.image_path = image_path
        self.color = color
        self.opacity = opacity
        self.playlist_path = playlist_path
        self.number_of_songs = number_of_songs