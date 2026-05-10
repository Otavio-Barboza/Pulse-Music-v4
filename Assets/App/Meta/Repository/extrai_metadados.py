from ..Models.musica_meta import MusicaMetadados
from mutagen import File
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, TXXX
from mutagen.mp3 import MP3
from pathlib import Path
import os, asyncio, requests

class ExtracaoMetadados:
    @classmethod
    def _async_extrair_metadados(cls, caminho_audio: str) -> dict[str | None]:
        """
        Extrai título, artista e capa do áudio (se existir).

        Retorna:
            dict {
                titulo: str | None
                artista: str | None
                capa_path: str | None
            }
        """
        from ...Services.gerenciador_contas import GerenciadorContas

        caminho_audio = Path(caminho_audio)
        pasta_capa = Path(f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Imagens/Capa Musica')
        pasta_capa.mkdir(parents = True, exist_ok = True)

        titulo = None
        artista = None
        capa_path = None

        audio = File(caminho_audio, easy=True)

        if audio:
            titulo = audio.get("title", [None])[0]
            artista = audio.get("artist", [None])[0]

        # Extração da capa (principalmente MP3)
        try:
            tags = ID3(caminho_audio)
            for tag in tags.values():
                if isinstance(tag, APIC):
                    capa_path = pasta_capa / f"{caminho_audio.stem}.jpg"
                    with open(capa_path, "wb") as img:
                        img.write(tag.data)
                    capa_path = str(capa_path)
                    break
        except Exception:
            pass  # Sem capa ou formato não suportado

        return {
            "titulo": titulo,
            "artista": artista,
            "capa": capa_path
        }

    @classmethod
    async def _async_organiza_dados(cls, nome_arquivo_original : str, titulo_filtrado : dict | None, artista_meta_nativo : str | None, status : str, id_playlist : str | None = None, id_artista : str = '') -> MusicaMetadados:
        """
            Organiza os dados retornados das filtragens e extrações de metadados
        Args:
            nome_arquivo_original (str): Nome integral do arquivo .mp3
            titulo_filtrado (dict | None): Dicionario do titulo filtrado senão None
            artista_meta_nativo (str | None): String do artista filtrado ou None
            status (str): String para denominar as operações seguintes

        Returns:
            dict[str | None]: Dicionário organizados com todas as informações
        """
        return MusicaMetadados(
            id_playlist = id_playlist,
            artista_id = id_artista,
            arquivo_mp3_original = nome_arquivo_original,
            titulo_musica_original = titulo_filtrado['titulo_original'] if titulo_filtrado is not None else None,
            titulo_musica_filtrado = titulo_filtrado['titulo_filtrado'] if titulo_filtrado is not None else None,
            artista_titulo_filtrado = titulo_filtrado['artista'] if titulo_filtrado is not None else None,
            artista_meta_nativo = artista_meta_nativo,
            status = status,
            arquivo_mp3_filtrado = None,
            artista_arquivo_filtrado = None,
            artista_final = None,
            score = None
        )

    @classmethod
    async def _async_extrair(cls, caminho : str):
        return await asyncio.to_thread(
            cls._async_extrair_metadados,
            caminho
        )
    
    #   -----   EDIÇÃO E CAPTAÇÃO DE METADADOS NOVOS    -----

    @classmethod
    def registrar_metadados_player(
        cls,
        caminho_arquivo: str,
        titulo: str,
        artista: str,
        album: str,
        id_art : str | None = None,
        url_img_artista_medium : str | None = None,
        url_img_artista_big : str | None = None,
        id_alb : str | None = None,
        url_img_album_medium: str | None = None,
        url_img_album_big: str | None = None,
    ):
        """
            Função para registar os dados obtidos do pipeline diretamente em metadados nativos nos arquivos.

        Args:
            caminho_arquivo (str): caminho completo do arquivo
            titulo (str): titulo final da filtragem
            artista (str): artista final atribuído
            album (str): álbum identificado
            url_img_artista_medium (str | None, optional): Imagem do artista identificado, caso exista. Defaults to None.
            url_img_artista_big (str | None, optional): Imagem do artista identificado, caso exista. Defaults to None.
            url_img_album_medium (str | None, optional): imagem do álbum identificado, caso exista. Defaults to None.
            url_img_album_big (str | None, optional): imagem do álbum identificado, caso exista. Defaults to None.
        """

        # abre o arquivo .mp3
        audio = MP3(caminho_arquivo, ID3 = ID3)

        # Se não tiver tags -> cria elas.
        try:
            audio.add_tags()
        except:
            pass
        
        # acessando as tags
        tags = audio.tags

        # limpar apenas textos antigos
        tags.delall("TIT2")
        tags.delall("TPE1")
        tags.delall("TALB")
        tags.delall("TXXX:PLAYER_PIPELINE")
        tags.delall("TXXX:PLAYER_ARTIST_ID")
        tags.delall("TXXX:PLAYER_ALBUM_ID")

        # limpar imagens do player (matém capa original)
        for tag in list(tags.values()):
            if isinstance(tag, APIC) and tag.desc.startswith('PLAYER_'):
                tags.delall(tag.HashKey)
                
        # escrever novos metadados
        tags.add(TIT2(encoding = 3, text = titulo))
        tags.add(TPE1(encoding = 3, text = artista))
        tags.add(TALB(encoding = 3, text = album))

        # -------- função download --------
        def baixar(url):
            """
                Baixa as imagens da API

            Args:
                url (str): link direcionado da API da Deezer da respectiva imagem

            Returns:
                str: bytes da imagem
            """
            
            try:
                r = requests.get(url, timeout=10)
                return r.content
            except:
                return None
        
        # _____ inserir imagem artista _____
        if url_img_artista_medium:
            img = baixar(url_img_artista_medium)
            
            if img:
                tags.add(APIC(
                    encoding = 3,
                    mime = 'image/jpeg',
                    type = 7,
                    desc = 'PLAYER_ARTIST_MEDIUM',
                    data = img   
                ))
        
        if url_img_artista_big:
            img = baixar(url_img_artista_big)
            
            if img:
                tags.add(APIC(
                    encoding = 3,
                    mime = 'image/jpeg',
                    type = 7,
                    desc = 'PLAYER_ARTIST_BIG',
                    data = img
                ))
            

        # _____ inserir imagem album _____
        if url_img_album_medium:
            img = baixar(url_img_album_medium)
            
            if img:
                tags.add(APIC(
                    encoding = 3,
                    mime = 'image/jpeg',
                    type = 4,
                    desc = 'PLAYER_ALBUM_MEDIUM',
                    data = img
                ))
                
        if url_img_album_big:
            img = baixar(url_img_album_big)
            
            if img:
                tags.add(APIC(
                    encoding = 3,
                    mime = 'image/jpeg',
                    type = 4,
                    desc = 'PLAYER_ALBUM_BIG',
                    data = img
                ))

        if id_art:
            tags.add(TXXX(
                encoding=3,
                desc="PLAYER_ARTIST_ID",
                text=str(id_art)
            ))

        if id_alb:
            tags.add(TXXX(
                encoding=3,
                desc="PLAYER_ALBUM_ID",
                text=str(id_alb)
            ))

        # campo validador
        tags.add(
            TXXX(
                encoding = 3,
                desc = "PLAYER_PIPELINE",
                text = "PROCESSADO"
            )
        )

        audio.save()

        print(f'Música finalizada (registro de metadados): {caminho_arquivo}')

    @classmethod
    def musica_ja_processada(cls, caminho: str) -> bool:
        """
            Verifica se o campo validador adicionado pela def registrar_metadados_player já alterou essa música em algum momento.

        Args:
            caminho (str): caminho completo do arquivo MP3

        Returns:
            bool: True | False
        """
        try:
            tags = ID3(caminho)

            if "TXXX:PLAYER_PIPELINE" in tags:
                return True

        except:
            pass

        return False
    
    @classmethod
    def extrair_metadados_player(cls, caminho_arquivo: str) -> dict:
        """
            Função para extrair os dados (metadados) que forma atribuídos manualmente pelo player

        Args:
            caminho_arquivo (str): caminho completo do arquivo MP3

        Returns:
            dict: dicionário contendo as informações extraídas do arquivo.
        """
        resultado = {
            "titulo": None,
            "artista": None,
            "album": None,
            "validador_pipeline": False,
            "capa_original": None,
            
            "id_artista" : None,
            "imagem_artista_medium": None,
            "imagem_artista_big": None,

            "id_album" : None,
            "imagem_album_player_medium": None,
            "imagem_album_player_big": None
        }

        audio = MP3(caminho_arquivo, ID3=ID3)
        tags = audio.tags

        if not tags:
            return resultado

        if "TIT2" in tags:
            resultado["titulo"] = str(tags["TIT2"])

        if "TPE1" in tags:
            resultado["artista"] = str(tags["TPE1"])

        if "TALB" in tags:
            resultado["album"] = str(tags["TALB"])

        if "TXXX:PLAYER_PIPELINE" in tags:
            resultado["validador_pipeline"] = True

        if "TXXX:PLAYER_ARTIST_ID" in tags:
            tag = tags["TXXX:PLAYER_ARTIST_ID"]
            if tag.text:
                resultado["id_artista"] = tag.text[0]

        if "TXXX:PLAYER_ALBUM_ID" in tags:
            tag = tags["TXXX:PLAYER_ALBUM_ID"]
            if tag.text:
                resultado["id_album"] = tag.text[0]
        
        # percorre todas as imagens existentes.
        for tag in tags.values():
            if isinstance(tag, APIC):
                if tag.type == 3:
                    resultado["capa_original"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                    
                # _____ artista _____
                elif tag.desc == 'PLAYER_ARTIST_MEDIUM':
                    resultado["imagem_artista_medium"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                elif tag.desc == 'PLAYER_ARTIST_BIG':
                    resultado["imagem_artista_big"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                
                # _____ album _____
                elif tag.desc == 'PLAYER_ALBUM_MEDIUM':
                    resultado["imagem_album_player_medium"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                elif tag.desc == 'PLAYER_ALBUM_BIG':
                    resultado["imagem_album_player_big"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }

        return resultado
    
    @classmethod
    def extrair_imagens_mp3(cls, caminho_arquivo: str, nome : dict, nome_capa : str):
        from ...Services.gerenciador_contas import GerenciadorContas
        from ..Repository.normalizacao import Filtragem

        """
            Extrai as imagens do arquivo MP3

        Args:
            caminho_arquivo (str): caminho completo do MP3
            pasta_destino (str): Pasta destinada a salvar as imagens
        """

        audio = MP3(caminho_arquivo, ID3 = ID3)
        tags = audio.tags

        if not tags:
            return

        dic = {}
        # percorre todas as imagens imbutidas no arquivo 
        for tag in tags.values():
            pasta_destino = None

            if isinstance(tag, APIC):
                # definir nome do arquivo
                conta = GerenciadorContas.contas_cache["conta_atual"]

                if tag.type == 3:
                    pasta_destino = f'Assets/Data/Contas/{conta}/Imagens/Capa Musica/{nome_capa}.jpg'
                    dic["capa"] = pasta_destino
                elif tag.desc == 'PLAYER_ARTIST_MEDIUM':
                    nome_norm = Filtragem.artista_base(nome.get("artista"))
                    pasta_destino = f'Assets/Data/Contas/{conta}/Imagens/Artistas/{nome_norm}.jpg'
                    dic["art"] = pasta_destino
                elif tag.desc == 'PLAYER_ALBUM_MEDIUM':
                    pasta_destino = f'Assets/Data/Contas/{conta}/Imagens/Albuns/{nome.get("album")}.jpg'
                    dic['alb'] = pasta_destino
                else:
                    continue

                # ext = '.png' if 'png' in tag.mime else '.jpg'
                caminho_saida = pasta_destino
                
                # grava a imagem no diretório
                with open(caminho_saida, "wb") as img:
                    img.write(tag.data)

        return dic
    
    @classmethod
    def carregar_imagem_big_base64(cls, caminho_arquivo : str, tipo : str):
        import base64
        
        """
            Função para carregar as imagens do tipo big sem salvá-las fisicamente em algum diretório do dispositivo.

        Args:
            caminho_arquivo (str): _description_
            tipo (str): _description_
        """
        
        audio = MP3(caminho_arquivo, ID3 = ID3)
        tags = audio.tags
        
        if not tags:
            return None
        
        alvo = {
            'artist' : 'PLAYER_ARTIST_BIG',
            'album' : 'PLAYER_ALBUM_BIG'
        }.get(tipo)
        
        for tag in tags.values():
            if isinstance(tag, APIC) and tag.desc == alvo:
                base64_str = base64.b64encode(tag.data).decode('utf-8')
                return base64_str
        return None