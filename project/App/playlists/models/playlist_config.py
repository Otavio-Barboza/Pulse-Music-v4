class PlaylistConfig:
    def __init__(
        self, 
        id,
        nome, 
        style,
        musicas,
        datas
    ):
        self.id = id
        self.style = style
        self.musicas = musicas
        self.datas = datas
        self.nome = nome

    # setters para atualização de informações na "memória" da classe (facilitando a att depois no JSON).
    def set_nome(self, nome):
        if not nome:
            raise ValueError("Nome inválido")
        self.nome = nome

    def set_cor(self, cor):
        self.style["cor"] = cor

    def set_opacidade(self, opacidade):
        self.style["opacidade"] = opacidade

    def set_imagem(self, imagem):
        self.style["pasta"] = imagem

    def set_pasta_musicas(self, pasta):
        self.musicas["pasta"] = pasta