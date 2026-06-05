from ...Services.gerenciador_contas import GerenciadorContas
import json

class LetraRepository:
    @classmethod
    def ler_json(cls) -> dict:
        with open(f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/letras.json', 'r', encoding = 'utf-8') as js:
            return json.load(js)
    
    @classmethod
    def salvar_json(cls, dados : dict):
        with open(f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/letras.json', 'w', encoding = 'utf-8') as js:
            json.dump(dados, js, indent = 4, ensure_ascii = False)