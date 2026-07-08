# imports de back-end
from project.core.services.account_manager import AccountManager
from project.core.utils.utils import Utils
from project.core.song.model.song import Song
from project.core.favorite.enum.favorite_enum import Favorited

# imports gerais
import json, os


class FavoriteRepository:

    CAMINHO_FAVORITAS = f'Assets/Data/Contas/{AccountManager.accounts_cache["current_account"]}/Song/favoritas.json'

    @classmethod
    def format_object_in_json(cls, data: Song, status: Favorited) -> str | dict[str, dict[str, str]]:
        from ...Audio.Model.modo_reproducao import ModoReprodução
        return data.chave, {
            'status' : status,
            'nome' : data.nome,
            'caminho' : data.caminho,
            'modo' : ModoReprodução.FAVORITA.value
        }

    @classmethod
    def list_favorite(cls) -> list[str]:
        favorite_json: dict = Utils.sync_load_json(cls.CAMINHO_FAVORITAS)
        favorite_keys: list[str] = []

        key: str

        for key, _ in favorite_json.items():
            if key not in favorite_keys:
                favorite_keys.append(key)

        return favorite_keys
    
    @classmethod
    def list_favorite_objects(cls) -> list[Song]:
        favorite_json: dict = Utils.sync_load_json(cls.CAMINHO_FAVORITAS)
        list_music: list[Song] = []
        
        key: str
        item: dict
        
        for key, item in favorite_json.items():
            list_music.append(
                Song(
                    key = key,
                    name = item.get('name'),
                    path = item.get('path'),
                    mode = item.get('mode')
                )
            )

        return list_music