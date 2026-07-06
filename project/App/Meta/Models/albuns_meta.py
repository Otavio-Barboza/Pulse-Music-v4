class MusicasAlbuns: 
    def __init__(self): 
        self.albuns : dict[str, dict] = {} 
        
    def adicionar_album(
        self, 
        caminho_musica : str, 
        chave_musica : str, 
        nome : str
    ):
        if nome not in self.albuns:
            self.albuns[nome] = {
                'musicas': []
            }
            self.albuns[nome]['musicas'].append({
                'chave_da_musica' : chave_musica,
                'caminho_da_musica_completa' : caminho_musica
            })
            
    def to_dict(self): 
        return self.albuns