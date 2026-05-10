from Assets.App.Meta.Controller.status import Status

class MusicaMetadados:
    def __init__(
        self,
        # IDs a serem salvos
        id_playlist : str,
        artista_id : str,
        
        # Elementos originais do arquivo (título e artista)
        arquivo_mp3_original : str,
        titulo_musica_original : str | None,
        artista_meta_nativo : str | None,

        # Elementos filtrados ou captados
        titulo_musica_filtrado : str | None,
        artista_titulo_filtrado : str | None,
        arquivo_mp3_filtrado : str | None,
        artista_arquivo_filtrado : str | None,

        artista_final : str | None,
        
        # Classificações do processo (sobretudo em casos que contém apenas o título, sem nenhuma referência de artista)
        score : float | int,
        status : Status,
        sim_1 : None | float = None,
        sim_2 : None | float = None,
        gap : None | float = None,
        consenso : None | float = None,

        caminho_musica : str | None = None,
        lista_artistas_possiveis : list[dict] | None = None,

        # Dados artista
        img_artista : dict = {
            'id_deezer' : None,
            'medium' : None, # str do caminho da img medium salva
            'big' : {
                'link' : None,
                'caminho' : None # str da musica sendo salva.
            } 
        },

        # Dados álbum
        img_album : dict = {
            'id' : None, 
            'nome' : None, 
            'medium' : None, 
            'big' : {
                'link' : None,
                'caminho' : None
            }
        }
    ):
        self.caminho = caminho_musica
        self.id_playlist = id_playlist
        self.id_artista = artista_id

        # nome do .mp3
        self.arquivo_mp3_original = arquivo_mp3_original
        self.arquivo_mp3_filtrado = arquivo_mp3_filtrado
        self.artista_arquivo_filtrado = artista_arquivo_filtrado
        
        # titulo extraído (ID3)
        self.titulo_musica_original = titulo_musica_original
        self.titulo_musica_filtrado = titulo_musica_filtrado
        self.artista_titulo_filtrado = artista_titulo_filtrado
        
        # artista estraido (ID3)
        self.artista_meta_nativo = artista_meta_nativo
        
        # Operação
        self.artista_final = artista_final
        self.score = score
        self.status = status

        # Operações apenas titulo
        self.sim_1 = sim_1
        self.sim_2 = sim_2
        self.gap = gap
        self.consenso = consenso
        self.lista_artistas_possiveis = lista_artistas_possiveis

        # Imagens
        self.img_artista = img_artista
        self.img_album = img_album

    def set_artista_final(self, artista : str):
        self.artista_final = artista
        
    def set_status(self, status : str):
        self.status = status
    
    def set_score(self, score : float | int):
        self.score = score
    
    def set_sim_1(self, sim_1 : None | float):
        self.sim_1 = sim_1
    
    def set_sim_2(self, sim_2 : None | float):
        self.sim_2 = sim_2
    
    def set_gap(self, gap : None | float):
        self.gap = gap

    def set_consenso(self, consenso : None | float):
        self.consenso = consenso
    
    def set_possiveis_artistas(self, artistas : list):
        self.lista_artistas_possiveis = artistas
    
    def set_arquivo_filtrado(self, arquivo_filt : str):
        self.arquivo_mp3_filtrado = arquivo_filt
    
    def set_artista_arquivo_filtrado(self, artista : str | None):
        self.artista_arquivo_filtrado = artista

    def set_imagem_artista(
        self, 
        id : str | None,
        img_m : str | None, # caminho
        img_b : str | None, # caminho_arquivo
        img_b_link : str | None
    ):
        self.img_artista = {
            'id' : id,
            'medium' : img_m,
            'big' : {
                'link' : img_b_link,
                'caminho' : img_b
            }
        }

    def set_imagem_album(
        self, 
        nome : str | None,
        id : str | None,
        img_m : str | None,
        img_b : str | None,
        img_b_link : str | None
    ):
        self.img_album = {
            'id' : id,
            'nome' : nome,
            'medium' : img_m,
            'big' : {
                'link' : img_b_link,
                'caminho' : img_b
            }
        }
        
    def set_caminho(self, caminho : str):
        self.caminho = caminho

    def set_artista_id(self, id : str):
        self.id_artista = id