import os, json
from typing import Callable

class Usuario:
    def __init__(self, id_conta, pasta_base, nome, email, imagem):
        self._id_conta = id_conta
        self._pasta_base = pasta_base
        self._nome = nome
        self._email = email
        self._imagem = imagem
        self._callbacks = []
        self._dirty = False

    # properties (encapsulamento)
    @property
    def id(self) -> str:
        return self._id_conta
    
    @property
    def pasta_base(self) -> str:
        return self._pasta_base
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, valor : str):
        if valor is None:
            return
        
        if valor != self._nome:
            self._nome = valor
            self._dirty = True
            self._executar_callbacks()

    @property
    def email(self) -> str:
        return self._email
    
    @property
    def imagem(self) -> str:
        return self._imagem

    @imagem.setter
    def imagem(self, valor : str):
        if valor is None:
            return
        
        if valor != self._imagem:
            self._imagem = valor
            self._dirty = True
            self._executar_callbacks()
    
    # callbacks
    def registrar_callback(self, func : callable):
        if callable(func):
            self._callbacks.append(func)

    def _executar_callbacks(self):
        for func in self._callbacks:
            try:
                func(self)
            except Exception:
                pass
    
    # carregar
    def retorna_dict(self) -> dict:
        return {
            'id' : self._id_conta,
            'nome' : self._nome,
            "email" : self._email,
            "imagem" : self._imagem
        }

    def salvar(self):
        """
            Função para salvar os dados no perfil.json quando uma nova conta é criada.
        """
        caminho = os.path.join(self._pasta_base, 'perfil.json')
        os.makedirs(self._pasta_base, exist_ok=True)

        with open(caminho, 'w', encoding = 'utf-8') as js:
            json.dump(self.retorna_dict(), js, indent = 4, ensure_ascii = False)
        self._dirty = True

    def carregar_perfil_json(cls, pasta_base : str):
        """
            Função para carregar o perfil.json

        Args:
            pasta_base (str): pasta da conta + perfil.json

        Returns:
            None | dict : nada ou dicionário com os dados do perfil.json
        """
        caminho = os.path.join(pasta_base, "perfil.json")

        if not os.path.exists(caminho):
            return None
        with open(caminho, "r", encoding="utf-8") as js:
            return json.load(js)