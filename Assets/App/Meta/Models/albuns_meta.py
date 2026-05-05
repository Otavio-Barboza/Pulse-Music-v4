class MusicasAlbuns: 
    def __init__(self): 
        self.albuns : dict[str, dict] = {} 
        
    def adicionar_album(self, caminho_musica : str, nome : str):
        if nome not in self.albuns:
            self.albuns[nome] = {
                'musicas': []
            }

            self.albuns[nome]['musicas'].append(caminho_musica)
            
    def to_dict(self): 
        return self.albuns