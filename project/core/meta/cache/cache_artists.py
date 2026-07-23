# imports de back-end
from core.meta.repository.filtering import Filtering
from core.meta.repository.metadata_repository import MetadataRepository

# imports gerais
from uuid import uuid4
from difflib import SequenceMatcher


class CacheArtists:

    cache_id = {}
    index_name = {}

    @classmethod
    async def load(cls):
        data = await MetadataRepository.return_artists_json()

        cls.cache_id = data
        cls.index_name = {}

        for artist_id, artist in data.items():
            name = artist['name']

            cls.index_name[name] = artist_id

            for alias in artist.get('aliases', []):
                cls.index_name[alias] = artist_id
    
    @classmethod
    async def save(cls):
        await MetadataRepository.save_artists_json(cls.cache_id)

    @classmethod
    def resolve_id(cls, name_org: str | None) -> str:
        if name_org is None:
            return None
        
        name = cls._normalize(name_org)

        if name in cls.index_name:
            return cls.index_name[name]
        
        for existing_name, artist_id in cls.index_name.items():
            score = SequenceMatcher(
                None,
                name,
                existing_name
            ).ratio()

            if score >= 0.90:
                cls._add_alias(
                    artist_id,
                    name
                )
                return artist_id
        
        return cls._crate_artist(name)
    
    @classmethod
    def _crate_artist(cls, name: str) -> str:
        artist_id = uuid4().hex

        cls.cache_id[artist_id] = {
            'name' : name,
            'aliases' : [name]
        }

        cls.index_name[name] = artist_id

        return artist_id
    
    @classmethod
    def _add_alias(
        cls,
        artist_id: str,
        name: str
    ):
        aliases = cls.cache_id[artist_id]['aliases']

        if name not in aliases:
            aliases.append(name)

        cls.index_name[name] = artist_id

    @classmethod
    def _normalize(cls, name: str) -> str:
        return Filtering.base_artist(
            Filtering.clean_feat(name)
        ).lower().strip()