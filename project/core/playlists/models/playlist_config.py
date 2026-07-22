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
    def set_name(self, name):
        if not name:
            raise ValueError("Nome inválido")
        self.name = name

    def set_color(self, color):
        self.style["color"] = color

    def set_opacity(self, opacity):
        self.style["opacity"] = opacity

    def set_image_path(self, image_path):
        self.style["image_path"] = image_path

    def set_music_path(self, pasta):
        self.music["music_path"] = pasta