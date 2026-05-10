from ..Models.musica_meta import MusicaMetadados
import json, aiofiles, hashlib, aiohttp, os

class GerenciaMetadados:
    @classmethod
    def _organizar_json_musicas(cls, musica : MusicaMetadados) -> dict:
        return {
            'id_playlist' : musica.id_playlist,
            'caminho' : musica.caminho,
            'arquivo_original' : musica.arquivo_mp3_original,
            'titulo_ID3_original' : musica.titulo_musica_original,
            'artista_final' : musica.artista_final,
            'artista_id' : musica.id_artista,

            'nome_musica_filtrado' : {
                'arquivo_mp3_filtrado' : musica.arquivo_mp3_filtrado,
                'titulo_ID3_filtrado' : musica.titulo_musica_filtrado
            },

            'artista_filtrado' : {
                'artista_arquivo_mp3' : musica.artista_arquivo_filtrado,
                'artista_titulo_ID3' : musica.artista_titulo_filtrado,
                'artista_ID3_nativo' : musica.artista_meta_nativo
            },

            'artista' : {
                'id_artista_deezer' : musica.img_artista.get('id', None),
                'img_medium' : musica.img_artista['medium'],
                'img_big' : musica.img_artista['big']
            },

            'album' : {
                'nome_album' : musica.img_album['nome'],
                'id_album_deezer' : musica.img_album['id'],
                'img_medium' : musica.img_album['medium'],
                'img_big' : musica.img_album['big']
            },

            'metricas' : {
                'score' : musica.score,
                'status' : musica.status,
                'gap' : musica.gap,
                'consenso' : musica.consenso,
                'sim_1' : musica.sim_1,
                'sim_2' : musica.sim_2
            }
        }
    
    @classmethod
    async def salvar_imagens(
        cls, 
        session : aiohttp.ClientSession, 
        url : str,
        caminho : str
    ):
        if not url:
            return None
        
        if os.path.exists(caminho):
            return caminho
        
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                conteudo = await resp.read()
            
            async with aiofiles.open(caminho, 'wb') as img:
                await img.write(conteudo)

            return caminho
        except Exception:
            return None
        
    @classmethod
    def gerar_track_id(cls, caminho : str):
        hasher = hashlib.sha1()
        with open(caminho, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()