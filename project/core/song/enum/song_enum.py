# import geral
from enum import Enum


class ReproductionMode(Enum):
    
    PLAYLIST = 'playlist'
    FAVORITE = 'favorite'
    ARTIST = 'artist'
    ALBUM = 'album'
    NOT_REPRODUCE = 'not_reproduce'