from Assets.App.Meta.Models.base import FonteMetadados
import aiohttp, asyncio

BASE_URL = 'https://api.deezer.com'

class GerenciadorFontes:
    def __init__(self, session):
        self.deezer = DeezerFonte(session)

# Classe é uma fonte de metadados e segue as regras da base
class DeezerFonte(FonteMetadados):
    def __init__(self, session : aiohttp.ClientSession):
        self.session = session

    async def _get(self, url, params = None):
        try:
            async with self.session.get(
                url, params = params, timeout = aiohttp.ClientTimeout(total = 12)
            ) as resp:
                resp.raise_for_status()
                return await resp.json()
        except asyncio.TimeoutError:
            return None
        except aiohttp.ClientError:
            return None
        
    async def buscar_musica(self, titulo : str, artista : str | None = None) -> dict:
        query = f'track:"{titulo}"'

        if artista:
            query += f' artist:"{artista}"'

        data = await self._get(
            f'{BASE_URL}/search',
            {'q' : query}
        )

        if data is None:
            return None
        
        return {
            'track' : data['data'],
            'fonte' : 'deezer',
        }
    
    async def buscar_album(self, album_id : int):
        return await self._get(f'{BASE_URL}/album/{album_id}')
    
    async def buscar_artista(self, artista_id : int):
        return await self._get(f'{BASE_URL}/artist/{artista_id}')