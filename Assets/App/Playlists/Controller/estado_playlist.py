from ..Repository.playlist_reprositorio import PlaylistRepositorio
from ...Services.gerenciador_contas import GerenciadorContas
from ..Models.playlist import Playlist
from ..Models.playlist_config import PlaylistConfig
from ..Repository.playlist_reprositorio import PlaylistRepositorio
from enum import Enum
import inspect, asyncio

class ModoOverlayPlaylist(Enum):
    CREATE = 'create'
    UPDATE = 'update'

class ModoPlaylist(Enum):
    GRID = "grid"
    LISTA = "lista"

class EstadoPlaylist:
    def __init__(self, grid):
        self.grid = grid
        self.lista_playlists = None
        self.playlist_config = None
        self.modo = ModoPlaylist.GRID

        self.imagem = r'Assets\Global\Images\Padrao\capa_playlist_padrao.png'
        self.nome = None
        self.cor = '#3d3d3d'
        self.opacidade = 1.0
        self.pasta = None
        self.qtde_mus = 0
        self.tipo = 'pasta'

    def criar_playlist(self):
        """
            Cria a playlist no back (JSONs e pasta) e no front (card)
        """
        play = PlaylistRepositorio.criar_playlist(
            nome = self.nome, 
            tipo = self.tipo,
            pasta_mus = self.pasta,
            origem_mus = 'pasta',
            cor = self.cor,
            pasta_img = self.imagem,
            opacidade = self.opacidade
        )

        self.grid.adicionar_playlist(
            playlist_id = play.id, 
            nome = self.nome, 
            qtde_mus = PlaylistRepositorio._count_musicas(self.pasta),
            cor = self.cor,
            img = self.imagem,
            path = self.pasta
        )
        
        return play.id
    
    def atualizar_playlist(self):
        """
            Função para atualizar os dados da playlist no UPDATE
        """        
        self.playlist_config.set_nome(self.nome)
        self.playlist_config.set_cor(self.cor)
        self.playlist_config.set_imagem(self.imagem)
        self.playlist_config.set_pasta_musicas(self.pasta)
        self.playlist_config.set_opacidade(self.opacidade)

        PlaylistRepositorio.salvar_config(self.playlist_config)

        # Atualiza o card no grid
        self.grid.atualizar_playlist(
            playlist_id = self.playlist_config.id,
            nome = self.nome,
            cor = self.cor,
            img = self.imagem,
            path = self.pasta,
            qtde_mus = PlaylistRepositorio._count_musicas(self.pasta)
        )

        PlaylistRepositorio.remover_conteudo_morto(
            id_playlist = self.playlist_config.id,
            pasta = self.pasta
        )

    def carregar_playlists(self):
        """
            Carrega cada card na inicilização do App
        """
        self.lista_playlists = PlaylistRepositorio.listar_playlists()

        for l in self.lista_playlists:
            self.grid.adicionar_playlist(
                playlist_id = l.id,
                nome = l.nome,
                cor = l.cor,
                img = l.caminho_imagem,
                path = l.pasta_play,
                qtde_mus = l.qtde_musicas
            )

    def abrir_config_playlist(self, playlist_id):
        """
            Abertura da playlist para o UPDATE, salvando os dados em memória no objeto self.playlist_config : PlaylistConfig()
        "Args" :
            playlist_id (str): ID da playlist 
        """
        usuario = GerenciadorContas.contas_cache
        caminho = f'Assets/Data/Contas/{usuario["conta_atual"]}/Playlists/{playlist_id}/config_play.json'

        dados = PlaylistRepositorio.ler_json(caminho)

        self.playlist_config = PlaylistConfig(
            id = dados['id'],
            style = dados['style'],
            musicas = dados['musicas'],
            datas = dados['datas'],
            nome = dados['nome']
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

        PlaylistRepositorio.escluir_playlist(playlist_id)
    
    def _retornar_imagens(self) -> list[str] | tuple[str, str]:
        """
            Intermédio para retorno das imagens ao Overlay
        Returns:
            list[str] | tuple[str, str]: Duas listas de imagens e uma tupla com os caminhos dos abuns e capas
        """
        return PlaylistRepositorio._retornar_imgs()
    
    def retornar_playlists_existentes(self) -> list[str]:
        return PlaylistRepositorio.verificar_nomes_playlists()
    
    def retornar_pastas_existentes(self) -> list[str]:
        return PlaylistRepositorio.verificar_pastas_existentes()

class EstadoPlay:
    _playlist_aberta = None
    _callbacks = {}

    @classmethod
    def registar_callback(cls, evento : str, funcao : callable):
        if evento not in cls._callbacks:
            cls._callbacks[evento] = []
        cls._callbacks[evento].append(funcao)
        
    @classmethod
    def notificar(cls, evento : str, dados = None):
        if evento not in cls._callbacks:
            return
        
        for func in cls._callbacks[evento]:
            try:
                if inspect.iscoroutinefunction(func):
                    asyncio.create_task(func(dados))
                else:
                    res = func(dados)
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception as e:
                import traceback
                print(f"[CALLBACK ERROR]: {e}")
                traceback.print_exc()

    @classmethod
    def abrir_playlist(cls, id_playlist : str, status : bool):
        cls._playlist_aberta = {
            'id' : id_playlist,
            'aberta' : status
        }

    @classmethod
    def fechar_playlist(cls):
        cls._playlist_aberta = None