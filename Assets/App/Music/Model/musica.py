class Musica:
    def __init__(
        self,
        caminho : str,
        nome : str,
        id : str,
        nome_filtrado : str = '',
        duracao : str = r'',
        artista : str = '',
        album : str = r'',
        capa : str = r''
    ):
        self.id = id
        self.nome = nome
        self.nome_filtrado = nome_filtrado
        self.caminho = caminho
        self.duracao = duracao
        self.artista = artista
        self.album = album
        self.capa = capa

    def set_nome_filtrado(self, nome : str):
        self.nome_filtrado = nome
        
    def set_duracao(self, duracao : str):
        self.duracao = duracao
    
    def set_artista(self, artista : str):
        self.artista = artista

    def set_album(self, album : str):
        self.album = album

    def set_capa(self, capa : str):
        self.capa = capa