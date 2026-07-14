# mport de back-end
from project.core.meta.models.song import SongMetadata
from project.core.services.account_manager import AccountManager

# imports gerais
from mutagen import File
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, TXXX
from mutagen.mp3 import MP3
from pathlib import Path
import asyncio, requests


class ExtractMetadata:

    @classmethod
    def async_extract_metadata(cls, path: str | Path) -> dict[str | None]:
        """
        Extrai título, artist e capa do áudio (se existir).

        Retorna:
            dict {
                title: str | None
                artist: str | None
                cover_path: str | None
            }
        """

        audio_path = Path(path)
        cover_destination = Path(f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Imagens/Capa Musica')
        cover_destination.mkdir(parents = True, exist_ok = True)

        title = None
        artist = None
        cover_path = None

        audio = File(audio_path, easy=True)

        if audio:
            title = audio.get("title", [None])[0]
            artist = audio.get("artist", [None])[0]

        # Extração da capa (principalmente MP3)
        try:
            tags = ID3(audio_path)
            for tag in tags.values():
                if isinstance(tag, APIC):
                    cover_path = cover_destination / f"{audio_path.stem}.jpg"
                    with open(cover_path, "wb") as img:
                        img.write(tag.data)
                    cover_path = str(cover_path)
                    break
        except Exception:
            pass  # Sem capa ou formato não suportado

        return {
            "title": title,
            "artist": artist,
            "capa": cover_path
        }

    @classmethod
    async def async_organize_data(
        cls, 
        mp3_file : str, 
        song_metadata_id3 : dict | None, 
        original_artist_id3 : str | None, 
        status : str, 
        playlist_id : str | None = None, 
        artist_id : str = ''
    ) -> SongMetadata:
        """
            Organiza os dados retornados das filtragens e extrações de metadados
        Args:
            mp3_file (str): Nome integral do arquivo .mp3
            titulo_filtrado (dict | None): Dicionario do title filtrado senão None
            artista_meta_nativo (str | None): String do artist filtrado ou None
            status (str): String para denominar as operações seguintes

        Returns:
            dict[str | None]: Dicionário organizados com todas as informações
        """
        return SongMetadata(
            playlist_id = playlist_id,
            artist_id = artist_id,
            mp3_file = mp3_file,

            original_song_title = song_metadata_id3["original_title"] if song_metadata_id3 is not None else None,
            song_title_id3_filtered = song_metadata_id3["title_filtered"] if song_metadata_id3 is not None else None,
            song_artist_id3_filtered = song_metadata_id3["artist"] if song_metadata_id3 is not None else None,
            original_artist_id3 = original_artist_id3,

            status = status,
            mp3_file_title = None,
            mp3_file_artist = None,
            defined_artist = None,
            score = None
        ) 
        # SongMetadata(
        #     id_playlist = id_playlist,
        #     artista_id = id_artista,
        #     arquivo_mp3_original = nome_arquivo_original,

        #     titulo_musica_original = titulo_filtrado['titulo_original'] if titulo_filtrado is not None else None,
        #     titulo_musica_filtrado = titulo_filtrado['titulo_filtrado'] if titulo_filtrado is not None else None,
        #     artista_titulo_filtrado = titulo_filtrado['artist'] if titulo_filtrado is not None else None,
        #     artista_meta_nativo = artista_meta_nativo,
            
        #     status = status,
        #     arquivo_mp3_filtrado = None,
        #     artista_arquivo_filtrado = None,
        #     artista_final = None,
        #     score = None
        # )

    @classmethod
    async def async_extract(cls, path: Path):
        return await asyncio.to_thread(
            cls._async_extrair_metadados,
            path
        )
    

    #   -----   EDIÇÃO E CAPTAÇÃO DE METADADOS NOVOS    -----
    @classmethod
    def register_metadata_player(
        cls,
        file_path: str,
        title: str,
        artist: str,
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
            file_path (str): caminho completo do arquivo
            title (str): title final da filtragem
            artist (str): artist final atribuído
            album (str): álbum identificado
            url_img_artista_medium (str | None, optional): Imagem do artist identificado, caso exista. Defaults to None.
            url_img_artista_big (str | None, optional): Imagem do artist identificado, caso exista. Defaults to None.
            url_img_album_medium (str | None, optional): imagem do álbum identificado, caso exista. Defaults to None.
            url_img_album_big (str | None, optional): imagem do álbum identificado, caso exista. Defaults to None.
        """

        # abre o arquivo .mp3
        audio = MP3(file_path, ID3 = ID3)

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
        tags.add(TIT2(encoding = 3, text = title))
        tags.add(TPE1(encoding = 3, text = artist))
        tags.add(TALB(encoding = 3, text = album))

        # -------- função download --------
        def download(url):
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
        
        # _____ inserir imagem artist _____
        if url_img_artista_medium:
            img = download(url_img_artista_medium)
            
            if img:
                tags.add(APIC(
                    encoding = 3,
                    mime = 'image/jpeg',
                    type = 7,
                    desc = 'PLAYER_ARTIST_MEDIUM',
                    data = img   
                ))
        
        if url_img_artista_big:
            img = download(url_img_artista_big)
            
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
            img = download(url_img_album_medium)
            
            if img:
                tags.add(APIC(
                    encoding = 3,
                    mime = 'image/jpeg',
                    type = 4,
                    desc = 'PLAYER_ALBUM_MEDIUM',
                    data = img
                ))
                
        if url_img_album_big:
            img = download(url_img_album_big)
            
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

        print(f'Música finalizada (registro de metadados): {file_path}')

    @classmethod
    def music_already_processed(cls, caminho: str) -> bool:
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
    def extract_metadata_playter(cls, file_path: str) -> dict:
        """
            Função para extrair os dados (metadados) que forma atribuídos manualmente pelo player

        Args:
            file_path (str): caminho completo do arquivo MP3

        Returns:
            dict: dicionário contendo as informações extraídas do arquivo.
        """
        result = {
            "title": None,
            "artist": None,
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

        audio = MP3(file_path, ID3=ID3)
        tags = audio.tags

        if not tags:
            return result

        if "TIT2" in tags:
            result["title"] = str(tags["TIT2"])

        if "TPE1" in tags:
            result["artist"] = str(tags["TPE1"])

        if "TALB" in tags:
            result["album"] = str(tags["TALB"])

        if "TXXX:PLAYER_PIPELINE" in tags:
            result["validador_pipeline"] = True

        if "TXXX:PLAYER_ARTIST_ID" in tags:
            tag = tags["TXXX:PLAYER_ARTIST_ID"]
            if tag.text:
                result["id_artista"] = tag.text[0]

        if "TXXX:PLAYER_ALBUM_ID" in tags:
            tag = tags["TXXX:PLAYER_ALBUM_ID"]
            if tag.text:
                result["id_album"] = tag.text[0]
        
        # percorre todas as imagens existentes.
        for tag in tags.values():
            if isinstance(tag, APIC):
                if tag.type == 3:
                    result["capa_original"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                    
                # _____ artist _____
                elif tag.desc == 'PLAYER_ARTIST_MEDIUM':
                    result["imagem_artista_medium"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                elif tag.desc == 'PLAYER_ARTIST_BIG':
                    result["imagem_artista_big"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                
                # _____ album _____
                elif tag.desc == 'PLAYER_ALBUM_MEDIUM':
                    result["imagem_album_player_medium"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }
                elif tag.desc == 'PLAYER_ALBUM_BIG':
                    result["imagem_album_player_big"] = {
                        "mime": tag.mime,
                        "tamanho_bytes": len(tag.data)
                    }

        return result
    
    @classmethod
    def extact_images_mp3(cls, file_path: str, name : dict, nome_capa : str, artista_id : str | None = None):
        """
            Extrai as imagens do arquivo MP3

        Args:
            file_path (str): caminho completo do MP3
            destination_path (str): Pasta destinada a salvar as imagens
        """

        audio = MP3(file_path, ID3 = ID3)
        tags = audio.tags

        if not tags:
            return

        dic = {}
        # percorre todas as imagens imbutidas no arquivo 
        for tag in tags.values():
            destination_path = None

            if isinstance(tag, APIC):
                # definir name do arquivo
                conta = AccountManager.contas_cache["conta_atual"]

                if tag.type == 3:
                    destination_path = f'Assets/Data/Contas/{conta}/Imagens/Capa Musica/{nome_capa}.jpg'
                    dic["capa"] = destination_path
                elif tag.desc == 'PLAYER_ARTIST_MEDIUM':
                    destination_path = f'Assets/Data/Contas/{conta}/Imagens/Artistas/{artista_id}.jpg'
                    dic["art"] = destination_path
                elif tag.desc == 'PLAYER_ALBUM_MEDIUM':
                    destination_path = f'Assets/Data/Contas/{conta}/Imagens/Albuns/{name.get("album")}.jpg'
                    dic['alb'] = destination_path
                else:
                    continue

                # grava a imagem no diretório
                with open(destination_path, "wb") as img:
                    img.write(tag.data)

        return dic
    
    @classmethod
    def load_image_big_base64(cls, file_path: str, type: str):
        import base64
        
        """
            Função para carregar as imagens do type big sem salvá-las fisicamente em algum diretório do dispositivo.

        Args:
            file_path (str): _description_
            type (str): _description_
        """
        
        audio = MP3(file_path, ID3 = ID3)
        tags = audio.tags
        
        if not tags:
            return None
        
        alvo = {
            'artist' : 'PLAYER_ARTIST_BIG',
            'album' : 'PLAYER_ALBUM_BIG'
        }.get(type)
        
        for tag in tags.values():
            if isinstance(tag, APIC) and tag.desc == alvo:
                base64_str = base64.b64encode(tag.data).decode('utf-8')
                return base64_str
        return None