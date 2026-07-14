# imports de back-end
from project.core.meta.repository.tasks import Task
from project.core.meta.enum.status import SongStatus
from project.core.meta.models.song import SongMetadata
from project.core.meta.repository.extract_metadata import ExtractMetadata


class Phase1:

    @classmethod
    async def phase_1(
        cls, 
        nome_arquivo_original : str, 
        titulo_filtrado : dict | None, 
        artista_meta_nativo : str | None
    ) -> SongMetadata:
        score = Task.similarity(
            b = artista_meta_nativo.strip().lower(),
            a = titulo_filtrado["artist"].strip().lower()
        )

        if score >= 0.85:
            return await ExtractMetadata.async_organize_data(
                nome_arquivo_original = nome_arquivo_original,
                titulo_filtrado = titulo_filtrado,
                artista_meta_nativo = artista_meta_nativo,
                status = SongStatus.BOTH
            )
        elif 0.65 <= score < 0.85:
            return await ExtractMetadata.async_organize_data(
                nome_arquivo_original = nome_arquivo_original,
                titulo_filtrado = titulo_filtrado,
                artista_meta_nativo = artista_meta_nativo,
                status = SongStatus.MEDIUM
            )
        else:
            return await ExtractMetadata.async_organize_data(
                nome_arquivo_original = nome_arquivo_original,
                titulo_filtrado = titulo_filtrado,
                artista_meta_nativo = artista_meta_nativo,
                status = SongStatus.INCONSISTENT    
            )