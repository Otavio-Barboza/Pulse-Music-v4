# imports de back-end
from core.utils.utils import Utils
from core.utils.path import AppPaths
from core.services.account_manager import AccountManager

# imports gerais
from pathlib import Path


class ServiceSettings:
    
    @classmethod
    def load_overlay(cls) -> True | False:
        path: Path = AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "settings.json"
        data: dict = Utils.sync_load_json(path)
        
        if data.keys():
            return data['overlays']['ON_overlay_playlist_size_tip']
        return None
    
    @classmethod
    def save_overlay_tips(cls, valor : bool):
        path: Path = AppPaths.ACCOUNT / AccountManager.accounts_cache["current_account"] / "settings.json"
        
        data: dict = Utils.sync_load_json(path)
        data['overlays']["ON_overlay_playlist_size_tip"] = valor

        Utils.sync_update_json(
            path = path,
            data = data
        ) 