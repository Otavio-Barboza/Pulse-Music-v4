# imports de back-end
from project.core.playlists.models.playlist_mode import PlaylistMode
from project.core.playlists.repository.playlist_reprositorio import PlaylistRepository

class PLaylistManager:
    def __init__(self, grid):
        self.grid = grid
        self.list_playlist = None
        self.playlist_config = None
        self.mode = PlaylistMode.GRID

        self.imagem = r'Assets\Global\Images\Padrao\capa_playlist_padrao.png'
        self.name = None
        self.color = '#3d3d3d'
        self.opacity = 1.0
        self.path = None
        self.number_of_songs = 0

    def criar_playlist(self):
        """
            Cria a playlist no back (JSONs e path) e no front (card)
        """
        play = PlaylistRepository.create_playlist(
            name = self.name, 
            tipo = self.tipo,
            pasta_mus = self.path,
            color = self.color,
            pasta_img = self.imagem,
            opacity = self.opacity
        )

        self.grid.adicionar_playlist(
            playlist_id = play.id, 
            name = self.name, 
            number_of_songs = PlaylistRepository._count_musicas(self.path),
            color = self.color,
            img = self.imagem,
            path = self.path
        )
        
        return play.id
    
    def atualizar_playlist(self):
        """
            Função para atualizar os dados da playlist no UPDATE
        """        
        self.playlist_config.set_nome(self.name)
        self.playlist_config.set_cor(self.color)
        self.playlist_config.set_imagem(self.imagem)
        self.playlist_config.set_pasta_musicas(self.path)
        self.playlist_config.set_opacidade(self.opacity)

        PlaylistRepository.salvar_config(self.playlist_config)

        # Atualiza o card no grid
        self.grid.atualizar_playlist(
            playlist_id = self.playlist_config.id,
            name = self.name,
            color = self.color,
            img = self.imagem,
            path = self.path,
            number_of_songs = PlaylistRepository._count_musicas(self.path)
        )

        PlaylistRepository.remover_conteudo_morto(
            id_playlist = self.playlist_config.id,
            path = self.path
        )

    def carregar_playlists(self):
        """
            Carrega cada card na inicilização do App
        """
        self.list_playlist = PlaylistRepository.listar_playlists()

        for l in self.list_playlist:
            self.grid.adicionar_playlist(
                playlist_id = l.id,
                name = l.name,
                color = l.color,
                img = l.caminho_imagem,
                path = l.pasta_play,
                number_of_songs = l.qtde_musicas
            )

    def abrir_config_playlist(self, playlist_id):
        """
            Abertura da playlist para o UPDATE, salvando os dados em memória no objeto self.playlist_config : PlaylistConfig()
        "Args" :
            playlist_id (str): ID da playlist 
        """
        usuario = AccountManager.accounts_cache
        caminho = f'Assets/Data/Contas/{usuario["current_account"]}/Playlists/{playlist_id}/config_play.json'

        dados = PlaylistRepository.ler_json(caminho)

        self.playlist_config = PlaylistConfig(
            id = dados['id'],
            style = dados['style'],
            musicas = dados['musicas'],
            datas = dados['datas'],
            name = dados['name']
        )

    def remover_playlist(self, playlist_id : str):
        """
            Remove a playlist graficamente (card) e chama o escluir_playlist do Repositorio para exclusão com uso do ID da playlist
        Args:
            playlist_id (str): ID da playlist
        """
        card = self.grid.cards.pop(playlist_id, None)

        if card:
            card.dispose()
            self.grid.controls.remove(card)
            self.grid.update()

        PlaylistRepository.escluir_playlist(playlist_id)
    
    def _retornar_imagens(self) -> list[str] | tuple[str, str]:
        """
            Intermédio para retorno das imagens ao Overlay
        Returns:
            list[str] | tuple[str, str]: Duas listas de imagens e uma tupla com os caminhos dos abuns e capas
        """
        return PlaylistRepository._retornar_imgs()
    
    def retornar_playlists_existentes(self) -> list[str]:
        return PlaylistRepository.verificar_nomes_playlists()
    
    def retornar_pastas_existentes(self) -> list[str]:
        return PlaylistRepository.verificar_pastas_existentes()