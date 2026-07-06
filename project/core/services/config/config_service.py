from ..gerenciador_contas import GerenciadorContas
import os, json

class ConfigService:
    @classmethod
    def ler_overlay(cls) -> True | False:
        dados = cls._ler()
        if dados.keys():
            return dados['Overlays']['ON_overlay_dica_tamanho_da_playlist']
        return None
    
    @classmethod
    def salvar_overlay_dicas(cls, valor : bool):
        dados = cls._ler()
        dados['Overlays']["ON_overlay_dica_tamanho_da_playlist"] = valor
        cls._salvar(dados)
    
    @classmethod
    def _ler(cls) -> dict:
        usuario = GerenciadorContas.contas_cache
        CAMINHO = f'Assets/Data/Contas/{usuario["conta_atual"]}/config.json'
        if not os.path.exists(CAMINHO):
            return {}
        with open(CAMINHO, 'r', encoding = 'utf-8') as js:
            return json.load(js)
        
    @classmethod
    def _salvar(cls, dados):
        usuario = GerenciadorContas.contas_cache
        CAMINHO = f'Assets/Data/Contas/{usuario["conta_atual"]}/config.json'
        with open(CAMINHO, 'w', encoding = 'utf-8') as js:
            json.dump(dados, js, indent = 4, ensure_ascii = False)