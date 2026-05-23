from ...Services.gerenciador_contas import GerenciadorContas
import json, os

class FavoritasRepository:
    CAMINHO_FAVORITAS = f'Assets/Data/Contas/{GerenciadorContas.contas_cache["conta_atual"]}/Music/favoritas.json'
    
    @classmethod
    def ler_json(cls) -> dict:
        with open(cls.CAMINHO_FAVORITAS, 'r', encoding = 'utf-8') as j:
            return json.load(j)
        
    @classmethod
    def salvar_json(cls, dados : dict):
        with open(cls.CAMINHO_FAVORITAS, 'w', encoding = 'utf-8') as j:
            json.dump(dados, j, ensure_ascii = False, indent = 4)

    @classmethod
    def formatar_objeto_no_json(cls, dado, status) -> str | dict[str, dict[str, str]]:
        from ...Audio.Model.modo_reproducao import ModoReprodução
        return dado.chave, {
            'status' : status,
            'nome' : dado.nome,
            'caminho' : dado.caminho,
            'modo' : ModoReprodução.FAVORITA.value
        }

    @classmethod
    def listar_favoritas(cls) -> list[str]:
        json_favoritas = cls.ler_json()
        chaves_favoritas = []

        for chave, _ in json_favoritas.items():
            if chave not in chaves_favoritas:
                chaves_favoritas.append(chave)

        return chaves_favoritas
    
    @classmethod
    def listar_objetos_favoritados(cls):
        from ...Audio.Model.musica import Musica

        json_favoritas = cls.ler_json()
        lista_musicas : list[Musica] = []

        for chave, item in json_favoritas.items():
            lista_musicas.append(
                Musica(
                    chave = chave,
                    nome = item.get('nome'),
                    caminho = item.get('caminho'),
                    modo = item.get('modo')
                )
            )

        return lista_musicas