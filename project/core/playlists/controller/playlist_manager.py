# imports de back-end
from project.core.utils.utils import Utils
from project.core.services.account_manager import AccountManager
from project.core.playlists.enum.playlist_enum import PlaylistMode
from project.core.playlists.repository.playlist_repository import PlaylistRepository
from project.core.playlists.models.playlist_config import PlaylistConfig

# import geral
from flet import GridView


class PlaylistManager:
    def __init__(self, grid: GridView):
        self.grid = grid
        self.list_playlist = None
        self.playlist_config = None
        self.mode = PlaylistMode.GRID

        self.image = r'Assets\Global\Images\Padrao\capa_playlist_padrao.png'
        self.name = None
        self.color = '#3d3d3d'
        self.opacity = 1.0
        self.path = None
        self.number_of_songs = 0

    def create_playlist(self):
        """
            Cria a playlist no back (JSONs e path) e no front (card)
        """
        playlist = PlaylistRepository.create_playlist(
            name = self.name, 
            music_path = self.path,
            color = self.color,
            image_path = self.image,
            opacity = self.opacity
        )

        self.grid.adicionar_playlist(
            playlist_id = playlist.id, 
            name = self.name, 
            number_of_songs = PlaylistRepository.count_number_of_songs(self.path),
            color = self.color,
            img = self.image,
            path = self.path
        )
        
        return playlist.id
    
    def update_playlist(self):
        """
            Função para atualizar os dados da playlist no UPDATE
        """    

        self.playlist_config.set_nome(self.name)
        self.playlist_config.set_cor(self.color)
        self.playlist_config.set_imagem(self.image)
        self.playlist_config.set_pasta_musicas(self.path)
        self.playlist_config.set_opacidade(self.opacity)

        PlaylistRepository.save_config(self.playlist_config)

        # Atualiza o card no grid
        self.grid.atualizar_playlist(
            playlist_id = self.playlist_config.id,
            name = self.name,
            color = self.color,
            img = self.image,
            path = self.path,
            number_of_songs = PlaylistRepository._count_musicas(self.path)
        )

        PlaylistRepository.remove_dead_content(
            id = self.playlist_config.id,
            path = self.path
        )

    def load_playlists(self):
        """
            Carrega cada card na inicilização do App
        """

        self.list_playlist = PlaylistRepository.listar_playlists()

        for playlist in self.list_playlist:
            self.grid.adicionar_playlist(
                playlist_id = playlist.id,
                name = playlist.name,
                color = playlist.color,
                img = playlist.image_path,
                path = playlist.playlist_path,
                number_of_songs = playlist.number_of_songs
            )

    def open_config_playlist(self, playlist_id: str):
        """
            Abertura da playlist para o UPDATE, salvando os dados em memória no objeto self.playlist_config : PlaylistConfig()
        "Args" :
            playlist_id (str): ID da playlist 
        """

        caminho = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Playlists/{playlist_id}/config_play.json'
        data: dict = Utils.sync_load_json(caminho)

        self.playlist_config = PlaylistConfig(
            id = data['id'],
            style = data['style'],
            music = data['musicas'],
            date = data['datas'],
            name = data['name']
        )

    def remove_playlist(self, playlist_id: str):
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

        PlaylistRepository.delete_playlist(playlist_id)
    
    def return_images(self) -> list[str] | tuple[str, str]:
        """
            Intermédio para retorno das imagens ao Overlay
        Returns:
            list[str] | tuple[str, str]: Duas listas de imagens e uma tupla com os caminhos dos abuns e capas
        """
        return PlaylistRepository.return_images()
    
    def return_existngs_playlists(self) -> list[str]:
        return PlaylistRepository.check_playlist_names()
    
    def return_existngs_playlists(self) -> list[str]:
        return PlaylistRepository.check_existing_folders()