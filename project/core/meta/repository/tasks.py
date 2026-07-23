# import de back-end
from core.meta.models.song import SongMetadata

# imports gerais
from pathlib import Path
from difflib import SequenceMatcher
import aiofiles, hashlib, aiohttp, os


class Task:

    @classmethod
    def return_song_json(cls, song: SongMetadata) -> dict:
        return {
            "song_path" : str(song.song_path),
            "playlist_id" : song.playlist_id,
            "artist_id" : song.artist_id,

            "mp3_file" : song.mp3_file,

            "mp3_file_filtered" : song.mp3_file_filtered,
            "id3_data" : song.id3_data,
            
            "defined_artist" : song.defined_artist,

            "artist" : song.artist_metadata,

            "album" : song.album_metadata,

            "metrics" : {
                "score" : song.score,
                "status" : song.status,
                "gap" : song.gap,
                "consensus" : song.consensus,
                "sim_1" : song.sim_1,
                "sim_2" : song.sim_2
            }
        }
    
    @classmethod
    async def save_image(
        cls, 
        session: aiohttp.ClientSession, 
        url: str,
        path: Path
    ):
        if not url:
            return None
        
        if os.path.exists(path):
            return path
        
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                conteudo = await resp.read()
            
            async with aiofiles.open(path, "wb") as img:
                await img.write(conteudo)

            return path
        except Exception:
            return None
        
    @classmethod
    def return_track_id(cls, path: Path):
        hasher = hashlib.sha1()

        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    @classmethod
    def similarity(cls, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()