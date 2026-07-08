from enum import Enum


class PlalistOverlayMode(Enum):
    CREATE = 'create'
    UPDATE = 'update'


class PlaylistMode(Enum):
    GRID = "grid"
    LIST = "list"


class PlaylistLoaded(Enum):
    OPEN = 'open'
    CLOSE = 'close'