# imports de back-end
from core.meta.repository.tasks import Task
from core.meta.enum.status import SongStatus
from core.meta.models.song import SongMetadata
from core.meta.repository.extract_metadata import ExtractMetadata


class Phase1:

    @classmethod
    async def phase_1(
        cls, 
        song_path,
        mp3_file: str, 
        song_metadata_id3: dict | None, 
        original_artist_id3: str | None,
        playlist_id: str | None
    ) -> SongMetadata:
        score = Task.similarity(
            b = original_artist_id3.strip().lower(),
            a = song_metadata_id3["artist"].strip().lower()
        )

        if score >= 0.85:
            return await ExtractMetadata.async_organize_data(
                mp3_file = mp3_file,
                song_metadata_id3 = song_metadata_id3,
                original_artist_id3 = original_artist_id3,
                status = SongStatus.BOTH,
                song_path = song_path,
                playlist_id = playlist_id
            )
        elif 0.65 <= score < 0.85:
            return await ExtractMetadata.async_organize_data(
                mp3_file = mp3_file,
                song_metadata_id3 = song_metadata_id3,
                original_artist_id3 = original_artist_id3,
                status = SongStatus.MEDIUM,
                song_path = song_path,
                playlist_id = playlist_id
            )
        else:
            return await ExtractMetadata.async_organize_data(
                mp3_file = mp3_file,
                song_metadata_id3 = song_metadata_id3,
                original_artist_id3 = original_artist_id3,
                status = SongStatus.INCONSISTENT,    
                song_path = song_path,
                playlist_id = playlist_id
            )