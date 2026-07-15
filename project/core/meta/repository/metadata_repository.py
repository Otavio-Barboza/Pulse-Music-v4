# import de back-end
from core.services.account_manager import AccountManager
from core.meta.repository.tasks import Task
from core.utils.utils import Utils
from core.meta.models.song import SongMetadata

# imports gerais
from pathlib import Path
import json, aiofiles, os, requests


class MetadataRepository:
    
    @classmethod
    async def data_manager_songs_json(cls, groups: dict):
        current_song_json: dict = await Utils.async_load_json(
            f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Music/musicas.json'
        )
        
        object_list = [
            musica
            for grupo in groups.values()
            for musica in grupo
        ]
        
        final_data = {}
        
        song: SongMetadata
        for song in object_list:            
            song_path = os.path.normpath(
                os.path.join(
                    song.song_path, 
                    song.mp3_file
                )
            )
            song_id = Task.return_track_id(song_path)
            
            final_data[song_id] = Task.return_song_json(
                song = song
            )
        
        for id, data in current_song_json.items():
            if id not in final_data:
                final_data[id] = data
        
        await Utils.async_update_json(path = cls.CAMINHO_CONTA_ATUAL, data = final_data)
    
    @classmethod
    async def load_cache(cls):
        from core.meta.cache.cache_artists import CacheArtists
        from core.meta.cache.global_cache import cache_metadata

        dados = await cls.ler_json(f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/musicas.json')
        cache_metadata.load(dados)

        await CacheArtists.load()

    @classmethod
    def download_image(cls, url: str, destination_path: Path | str) -> str | None:
        """
        Baixa uma imagem via URL e salva no caminho especificado.

        Args:
            url (str): URL da imagem
            destination_path (str): caminho completo (sem extensão ou com)

        Returns:
            str | None: caminho final salvo ou None se falhar
        """

        if not url:
            return None

        try:
            caminho = Path(destination_path)
            caminho.parent.mkdir(parents = True, exist_ok = True)

            response = requests.get(url, timeout=20)

            if response.status_code != 200:
                return None

            with open(caminho, "wb") as f:
                f.write(response.content)

            return str(caminho)
        except Exception as e:
            print("falha na conexão:", e)
            return None
    
    @classmethod
    def delete_image(cls, path: Path):
        try:
            if path and os.path.exists(path):
                os.remove(path)
                # print(f'Imagem removida: {path}')
            else:
                print(f'Imagem não encontrada: {path}')
        except Exception as erro:
            print(f'Erro ao remover a imagem: {erro}')

    
    # artistas
    @classmethod
    async def return_artists_json(cls) -> dict:
        return await Utils.async_load_json(
            f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/artistas.json'
        )
    
    @classmethod
    async def save_artists_json(cls, data: dict):
        await Utils.async_update_json(
            path = f'Assets/Data/Contas/{AccountManager.contas_cache["conta_atual"]}/Music/artistas.json',
            data = data
        )