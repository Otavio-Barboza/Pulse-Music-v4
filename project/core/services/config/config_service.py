from project.core.services.account_anager import AccountManager
import os, json

class ConfigService:
    
    @classmethod
    def ler_overlay(cls) -> True | False:
        data: dict = cls._ler()
        
        if data.keys():
            return data['Overlays']['ON_overlay_dica_tamanho_da_playlist']
        return None
    
    @classmethod
    def salvar_overlay_dicas(cls, valor : bool):
        data: dict = cls._ler()
        data['Overlays']["ON_overlay_dica_tamanho_da_playlist"] = valor
        cls._salvar(data)
    
    @classmethod
    def _ler(cls) -> dict:
        path: str = f'Assets/Data/Contas/{AccountManager.accounts_cache["conta_atual"]}/config.json'
        
        if not os.path.exists(path):
            return {}
        with open(path, 'r', encoding = 'utf-8') as js:
            return json.load(js)
        
    @classmethod
    def _salvar(cls, dados):
        path: str = f'Assets/Data/Contas/{AccountManager.accounts_cache["conta_atual"]}/config.json'
        
        with open(path, 'w', encoding = 'utf-8') as js:
            json.dump(dados, js, indent = 4, ensure_ascii = False)