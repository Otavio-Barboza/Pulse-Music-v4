class PlaylistConfig:
    def __init__(
        self, 
        id,
        name, 
        style,
        music,
        date
    ):
        self.id = id
        self.style = style
        self.music = music
        self.date = date
        self.name = name

    # setters para atualização de informações na "memória" da classe (facilitando a att depois no JSON).
    def set_nome(self, name):
        if not name:
            raise ValueError("Nome inválido")
        self.name = name

    def set_cor(self, cor):
        self.style["cor"] = cor

    def set_opacidade(self, opacidade):
        self.style["opacidade"] = opacidade

    def set_imagem(self, imagem):
        self.style["pasta"] = imagem

    def set_pasta_musicas(self, pasta):
        self.music["pasta"] = pasta