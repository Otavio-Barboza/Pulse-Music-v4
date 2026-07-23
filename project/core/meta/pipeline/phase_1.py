# imports de back-end
from core.meta.repository.tasks import Task
from core.meta.enum.status import SongStatus
from core.meta.models.song import SongMetadata
from core.meta.repository.extract_metadata import ExtractMetadata


class Phase1:

    @classmethod
    async def phase_1(
        cls, 
        mp3_file : str, 
        filtered_title : dict | None, 
        original_artist_id3 : str | None
    ) -> SongMetadata:
        score = Task.similarity(
            b = original_artist_id3.strip().lower(),
            a = filtered_title["artist"].strip().lower()
        )

        if score >= 0.85:
            return await ExtractMetadata.async_organize_data(
                mp3_file = mp3_file,
                filtered_title = filtered_title,
                original_artist_id3 = original_artist_id3,
                status = SongStatus.BOTH
            )
        elif 0.65 <= score < 0.85:
            return await ExtractMetadata.async_organize_data(
                mp3_file = mp3_file,
                filtered_title = filtered_title,
                original_artist_id3 = original_artist_id3,
                status = SongStatus.MEDIUM
            )
        else:
            return await ExtractMetadata.async_organize_data(
                mp3_file = mp3_file,
                filtered_title = filtered_title,
                original_artist_id3 = original_artist_id3,
                status = SongStatus.INCONSISTENT    
            )