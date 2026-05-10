from uuid import uuid4
from difflib import SequenceMatcher
from ..Repository.persistencia import Persistencia
from ..Repository.normalizacao import Filtragem
from ...Services.gerenciador_contas import GerenciadorContas

class MemoriaArtistas:
    cache_id = {}
    index_nome = {}

    @classmethod
    async def carregar(cls):
        data = await Persistencia.ler_artistas()

        cls.cache_id = data
        cls.index_nome = {}

        for artista_id, artista in data.items():
            nome = artista['nome']

            cls.index_nome[nome] = artista_id

            for alias in artista.get('aliases', []):
                cls.index_nome[alias] = artista_id
    
    @classmethod
    async def salvar(cls):
        await Persistencia.salvar_artistas(cls.cache_id)

    @classmethod
    def resolver_id(cls, nome_org : str) -> str:
        nome = cls._normalizar(nome_org)

        if nome in cls.index_nome:
            return cls.index_nome[nome]
        
        for nome_existente, artista_id in cls.index_nome.items():
            score = SequenceMatcher(
                None,
                nome,
                nome_existente
            ).ratio()

            if score >= 0.90:
                cls._adicionar_alias(
                    artista_id,
                    nome
                )
                return artista_id
        
        return cls._criar_artista(nome)
    
    @classmethod
    def _criar_artista(cls, nome : str) -> str:
        artista_id = uuid4().hex

        cls.cache_id[artista_id] = {
            'nome' : nome,
            'aliases' : [nome]
        }

        cls.index_nome[nome] = artista_id

        return artista_id
    
    @classmethod
    def _adicionar_alias(
        cls,
        artista_id : str,
        nome : str
    ):
        
        aliases = cls.cache_id[artista_id]['aliases']

        if nome not in aliases:
            aliases.append(nome)

        cls.index_nome[nome] = artista_id

    @classmethod
    def _normalizar(cls, nome : str) -> str:
        return Filtragem.artista_base(
            Filtragem._limpar_feat(
                nome
            )
        ).lower().strip()