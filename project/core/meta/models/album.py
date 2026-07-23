# import geral
from pathlib import Path


class Album: 

    def __init__(self): 
        self.albums : dict[str, dict] = {} 
        
    def add_album(
        self, 
        song_path: Path, 
        song_key: str, 
        name: str
    ):
        if name not in self.albums:
            self.albums[name] = {
                'songs': []
            }
            self.albums[name]['songs'].append({
                'key_song' : song_key,
                'destination_song' : song_path
            })
            
    def to_dict(self): 
        return self.albums