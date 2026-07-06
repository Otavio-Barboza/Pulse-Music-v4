from flet import Colors

class PlaylistCard:
    def __init__(
        self, 
        id : str, 
        nome : str, 
        caminho_imagem : str, 
        cor : Colors, 
        opacidade : float, 
        pasta_play : str,
        qtde_musicas : int
    ):
        self.id = id
        self.nome = nome
        self.caminho_imagem = caminho_imagem
        self.cor = cor
        self.opacidade = opacidade
        self.pasta_play = pasta_play
        self.qtde_musicas = qtde_musicas