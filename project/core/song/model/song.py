from core.song.enum.song_enum import ReproductionMode

class Song:
    def __init__(self, mode: ReproductionMode, name: str, path: str, key: str):
        self.name = name
        self.path = path
        self.key = key
        self.mode = mode