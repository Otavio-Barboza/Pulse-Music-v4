class Album: 

    def __init__(self): 
        self.albums : dict[str, dict] = {} 
        
    def add_album(
        self, 
        song_path : str, 
        song_key : str, 
        name : str
    ):
        if name not in self.albums:
            self.albums[name] = {
                'songs': []
            }
            self.albums[name]['songs'].append({
                'chave_da_musica' : song_key,
                'caminho_da_musica_completa' : song_path
            })
            
    def to_dict(self): 
        return self.albums