from ..Repository.validacao import Validacao
from Assets.App.Meta.Controller.status import Status
from ..Models.musica_meta import MusicaMetadados
from Assets.App.Meta.Repository.extrai_metadados import ExtracaoMetadados

class PipelineFase1:
    @classmethod
    async def _async_fase_1(cls, nome_arquivo_original : str, titulo_filtrado : dict | None, artista_meta_nativo : str | None) -> MusicaMetadados:
        score = Validacao.similaridade(
            b = artista_meta_nativo.strip().lower(),
            a = titulo_filtrado['artista'].strip().lower()
        )

        if score >= 0.85:
            return await ExtracaoMetadados._async_organiza_dados(
                nome_arquivo_original = nome_arquivo_original,
                titulo_filtrado = titulo_filtrado,
                artista_meta_nativo = artista_meta_nativo,
                status = Status.AMBOS
            )
        elif 0.65 <= score < 0.85:
            return await ExtracaoMetadados._async_organiza_dados(
                nome_arquivo_original = nome_arquivo_original,
                titulo_filtrado = titulo_filtrado,
                artista_meta_nativo = artista_meta_nativo,
                status = Status.MEDIO
            )
        else:
            return await ExtracaoMetadados._async_organiza_dados(
                nome_arquivo_original = nome_arquivo_original,
                titulo_filtrado = titulo_filtrado,
                artista_meta_nativo = artista_meta_nativo,
                status = Status.INCONSISTENTE    
            )