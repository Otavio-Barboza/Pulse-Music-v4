from ...Services.gerenciador_contas import GerenciadorContas
from ...Playlists.Repository.pastas import CreatePlaylist
from ...Playlists.Models.playlist import Playlist
from ...Playlists.Models.playlist_config import PlaylistConfig
from ...Playlists.Models.playlist_card import PlaylistCard
import json, os

class PlaylistRepositorio:
    @classmethod
    def ler_json(cls, cam) -> dict:
        with open(cam, 'r', encoding = 'utf-8') as js:
            return json.load(js)
    
    @classmethod
    def salvar_json(cls, cam : str, dados : dict):
        with open(cam, 'w', encoding = 'utf-8') as js:
            json.dump(dados, js, ensure_ascii = False, indent = 4)

    @classmethod
    def carregar_itens(cls) -> list[Playlist]:
        """
            Retorna uma lista com objetos Playlist() para auxiliar no carregamento das playlist ao rodar o app.
        Returns:
            list[Playlist]: lista com objetos Playlist().
        """
        lista_plays = []
        usuario = GerenciadorContas.contas_cache
        CAMINHO_JSON_PLAYLIST = f'Assets/Data/Contas/{usuario["conta_atual"]}/playlists.json'
        playlists = cls.ler_json(CAMINHO_JSON_PLAYLIST)

        for p in playlists['playlists']:
            if p != 'favoritas':
                id_play = playlists['playlists'].get(p)
                nome_play = id_play.get('nome')
                tipo_play = id_play.get('tipo')

                lista_plays.append(Playlist(
                    id = p,
                    nome = nome_play,
                    tipo = tipo_play
                ))
        
        return lista_plays
    
    @classmethod
    def carregar_cards(cls) -> list[PlaylistCard]:
        """
            Com auxílio do cls.carregar_itens utiliza-se dos objetos Playlist() e com eles carrega os detalhes de cada playlist, armazenando-os na lista cards os objetos PlaylistCard().
        Returns:
            list[PlaylistCard]: Lista com objetos PlaylistCard()
        """
        usuario = GerenciadorContas.contas_cache
        playlists = cls.carregar_itens()
        cards = []

        for pl in playlists:
            cfg = cls.ler_json(
                cam = f'Assets/Data/Contas/{usuario["conta_atual"]}/Playlists/{pl.id}/config_play.json'
            )
            
            caminho = cfg['musicas']['pasta']
            qtde = CreatePlaylist.contar_qtde_musicas(caminho)

            cards.append(PlaylistCard(
                id = pl.id,
                nome = cfg['nome'],
                caminho_imagem = cfg['style']['pasta'],
                cor = cfg['style']['cor'],
                opacidade = cfg['style']['opacidade'],
                pasta_play = caminho,
                qtde_musicas = qtde
            ))
        
        return cards
    
    @classmethod
    def listar_playlists(cls) -> list[PlaylistCard]:
        """
            Chama cls.carregar_cards para intermediar o retorno das playlists ao EstadoPlaylist
        Returns:
            list[PlaylistCard]: lista com objetos PlaylistCard()
        """
        return cls.carregar_cards()
    
    @classmethod
    def _count_musicas(cls, c : str) -> int:
        """
            Intermédio para EstadoPlaylist e outras chamadas do contador da quantidade de músicas da playlist.
        Args:
            c (str): caminho da pasta

        Returns:
            int: N° int da quantidade de músicas da playlist
        """
        return CreatePlaylist.contar_qtde_musicas(c)

    @classmethod
    def criar_playlist(
        cls, 
        nome : str, 
        tipo : str,
        pasta_mus : str,
        origem_mus : str,
        pasta_img : str,
        cor : str,
        opacidade : float

    ) -> Playlist:
        """
            Cria o objeto Playlist, a pasta, json da playlist e adição ao json playlists da existencia da playlist nova
        Args:
            nome (str): Nome da Plalist
            tipo (str): tipo (pasta ou fav)
            pasta_mus (str): caminho da pasta das musicas
            origem_mus (str): origem das musicas (pasta ou dinamica das favoritas)
            pasta_img (str): caminho da imagem
            cor (str): cor do bgcolor do card
            opacidade (float): valor da opacidade da cor

        Returns:
            Playlist: Objeto Playlist()
        """
        from pathlib import Path

        usuario = GerenciadorContas.contas_cache
        CAMINHO_JSON_PLAYLIST = f'Assets/Data/Contas/{usuario["conta_atual"]}/playlists.json'
        dados = cls.ler_json(CAMINHO_JSON_PLAYLIST)

        novo_id, id_num = CreatePlaylist.gerar_id(dados = dados)
        dados['ultimo_id'] = id_num
        
        PASTA_PLAYLIST = f'Assets/Data/Contas/{usuario["conta_atual"]}/Playlists/{novo_id}'
        JSON_CONFIG_PLAYLIST = f'Assets/Data/Contas/{usuario["conta_atual"]}/Playlists/{novo_id}/config_play.json'
        JSON_MUSICAS_PLAYLIST = f'Assets/Data/Contas/{usuario["conta_atual"]}/Music/musicas.json'
        qtde = CreatePlaylist.contar_qtde_musicas(pasta_mus)

        json_config = CreatePlaylist.retornar_conteudo_config_play_json(
            id = novo_id,
            pasta_mus = pasta_mus,
            pasta_img = pasta_img,
            cor = cor,
            origem_mus = origem_mus,
            opacidade = opacidade,
            nome = nome,
            qtde_mus = qtde
        )
        dados['playlists'][novo_id] = CreatePlaylist.retornar_conteudo_playlist_json(nome = nome, tipo = tipo)
        dados['ultima_atualizacao'] = CreatePlaylist.gerar_data()

        CreatePlaylist.criar_pasta(path = PASTA_PLAYLIST)
        CreatePlaylist.escrever_json(caminho = JSON_CONFIG_PLAYLIST, dados = json_config)
        
        if not Path(JSON_MUSICAS_PLAYLIST).exists():
            CreatePlaylist.escrever_json(caminho = 
        
        JSON_MUSICAS_PLAYLIST, dados = {})
        
        cls.salvar_json(cam = CAMINHO_JSON_PLAYLIST, dados = dados)

        return Playlist(
            id = novo_id,
            nome = nome,
            tipo = tipo,
            caminho = PASTA_PLAYLIST
        )

    @classmethod
    def _retornar_imgs(cls) -> list[str] | tuple[str, str]:
        """
            Intermedio ao EstadoPlaylist para a listagem de imagens 
        Returns:
            list[str] | tuple[str, str]: Lista das imagens e tupla com os caminhos dos albuns e capas
        """
        return CreatePlaylist._retornar_imagens_selecao()
    
    @classmethod
    def salvar_config(cls, playlist: PlaylistConfig):
        """
            Salva os dados do UPDATE da playlist em ambos JSONs
        Args:
            playlist (PlaylistConfig): Objeto PlaylistConfig para uso na inserção dos dados
        """
        usuario = GerenciadorContas.contas_cache
        caminho_config_json = f'Assets/Data/Contas/{usuario["conta_atual"]}/Playlists/{playlist.id}/config_play.json'
        caminho_play_json = f'Assets/Data/Contas/{usuario["conta_atual"]}/playlists.json'
 
        json_config = cls.ler_json(caminho_config_json)
        json_play = cls.ler_json(caminho_play_json)

        json_play['playlists'][playlist.id]['nome'] = playlist.nome
        json_play['ultima_atualizacao'] = CreatePlaylist.gerar_data()

        json_config['nome'] = playlist.nome
        json_config['style']['pasta'] = playlist.style['pasta']
        json_config['style']['cor'] = playlist.style['cor']
        json_config['style']['opacidade'] = playlist.style["opacidade"]
        json_config['musicas']['pasta'] = playlist.musicas['pasta']
        json_config['musicas']['quantidade_de_musicas'] = CreatePlaylist.contar_qtde_musicas(playlist.musicas['pasta'])
        json_config['datas']['ultima_atualizacao'] = CreatePlaylist.gerar_data()

        cls.salvar_json(cam = caminho_play_json, dados = json_play)
        cls.salvar_json(cam = caminho_config_json, dados = json_config)
    
    @classmethod
    def remover_play_do_json(cls, id : str):
        """
            Remove a playlist do indice no JSON playlists
        Args:
            id (str): ID da playlist
        """
        usuario = GerenciadorContas.contas_cache
        caminho = f'Assets/Data/Contas/{usuario["conta_atual"]}/playlists.json'
        dados = cls.ler_json(caminho)
        
        if id in dados['playlists']:
            dados['playlists'].pop(id)
            dados['ultima_atualizacao'] = CreatePlaylist.gerar_data()
        
        cls.salvar_json(cam = caminho, dados = dados)
        

    @classmethod
    def escluir_playlist(cls, id : str):
        """
            Função para executar a exclusão dos elementos da playlist
        Args:
            id (str): ID da Playlist
        """
        from ...Meta.Scanner.scanner import Scanner
        import asyncio
        
        caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists/{id}'
        leitura_json = cls.ler_json(f'{caminho}/config_play.json')

        pasta = leitura_json.get('musicas').get('pasta')
        
        chaves_para_remover = PlaylistRepositorio.reconhecer_chaves_das_musicas(id)

        asyncio.run(
            Scanner.reconhecer_artistas_albuns_inexistentes(
                chaves_remover = chaves_para_remover
            )
        )

        CreatePlaylist.remover_pasta(caminho)
        cls.remover_play_do_json(id = id)
        
    @classmethod
    def reconhecer_chaves_das_musicas(cls, id_playlist : str):
        json_musicas = cls.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json'
        )
        
        return {
            chave for chave, valor in json_musicas.items()
            if valor.get('id_playlist') == id_playlist
        }
    
    @classmethod
    def remover_conteudo_morto(cls, id_playlist : str, pasta : str):
        from ...Meta.Scanner.scanner import Scanner
        import asyncio

        chaves_para_remover = set()

        json_musicas = cls.ler_json(
            f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/musicas.json'
        )

        for chave, valor in json_musicas.items():
            if (
                valor.get('id_playlist') == id_playlist and
                valor.get('caminho') != pasta
            ):
                chaves_para_remover.add(chave)

        asyncio.run(
            Scanner.reconhecer_artistas_albuns_inexistentes(
                chaves_remover = chaves_para_remover
            )
        )

    @classmethod
    def verificar_nomes_playlists(cls) -> list[str]:
        caminho = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists'
        nomes_playlists_existentes = list()

        for c in os.listdir(
            caminho
        ):
            config_play_json = cls.ler_json(
                f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists/{c}/config_play.json'
            )

            nome = config_play_json.get('nome')

            if nome not in nomes_playlists_existentes:
                nomes_playlists_existentes.append(nome)

        return nomes_playlists_existentes
    
    @classmethod
    def verificar_pastas_existentes(cls) -> list[str]:
        caminho_base = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists'
        pastas_existentes = list()

        for playlist in os.listdir(
            caminho_base
        ):
            config_play_json = cls.ler_json(
                f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Playlists/{playlist}/config_play.json'
            )

            caminho_pasta = config_play_json['musicas'].get('pasta')

            if caminho_pasta not in pastas_existentes:
                pastas_existentes.append(caminho_pasta)

        return pastas_existentes