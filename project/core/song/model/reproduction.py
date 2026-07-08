# import de back-end
from project.core.song.model.song import Music
from project.core.song.enum.song_enum import ReproductionMode


class Reproduction:

    _lists_modes_playbacks: dict[ReproductionMode, list[Music]] = {
        ReproductionMode.PLAYLIST : [],
        ReproductionMode.FAVORITE : [],
        ReproductionMode.ARTIST : [],
        ReproductionMode.ALBUM : []
    }
    current_reproduction: ReproductionMode = ReproductionMode.NOT_REPRODUCE

    @classmethod
    def set_current_reproduction(cls, new_mode: ReproductionMode):
        cls.current_reproduction = new_mode

    @classmethod
    def return_current_reproduction(cls) -> ReproductionMode:
        return cls.current_reproduction
    
    @classmethod
    def load_songs_from_mode(cls, mode: ReproductionMode, list: list[Music]):
        if not list:
            return
        
        cls._lists_modes_playbacks[mode].clear()
        cls._lists_modes_playbacks[mode].extend(list)

    @classmethod
    def return_songs_for_mode(cls) -> list[Music]:
        if cls.current_reproduction != ReproductionMode.NOT_REPRODUCE:
            return cls._lists_modes_playbacks[cls.current_reproduction]
        return None

    # FUNÇÕES APENAS PARA AS FAVORITAS
    @classmethod
    def add_song(cls, song: Music):
        if song not in cls._lists_modes_playbacks[ReproductionMode.FAVORITE]:
            cls._lists_modes_playbacks[ReproductionMode.FAVORITE].append(song)
    
    @classmethod
    def remove_song(cls, song: Music):
        favorited_song: Music

        for favorited_song in cls._lists_modes_playbacks[ReproductionMode.FAVORITE]:
            if favorited_song.key == song.key:
                song_to_remove = favorited_song
                break

        cls._lists_modes_playbacks[ReproductionMode.FAVORITE].remove(song_to_remove)