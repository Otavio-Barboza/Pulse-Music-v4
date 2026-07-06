import os, json
from typing import Callable

class User:
    def __init__(self, account_id: str, base_path: str, name: str, email: str, image: str):
        self._account_id = account_id
        self._base_path = base_path
        self._name = name
        self._email = email
        self._image = image
        self._callbacks = []
        self._dirty = False

    # properties (encapsulamento)
    @property
    def id(self) -> str:
        return self._account_id
    
    @property
    def base_path(self) -> str:
        return self._base_path
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, valor : str):
        if valor is None:
            return
        
        if valor != self._name:
            self._name = valor
            self._dirty = True
            self._executar_callbacks()

    @property
    def email(self) -> str:
        return self._email
    
    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, valor : str):
        if valor is None:
            return
        
        if valor != self._image:
            self._image = valor
            self._dirty = True
            self._executar_callbacks()
    
    # callbacks
    def register_callback(self, func : callable):
        if callable(func):
            self._callbacks.append(func)

    def notify_callbacks(self):
        for func in self._callbacks:
            try:
                func(self)
            except Exception:
                pass
    
    # carregar
    def return_dict(self) -> dict[str, str]:
        return {
            'id' : self._account_id,
            'nome' : self._name,
            "email" : self._email,
            "imagem" : self._image
        }

    def save_json(self):
        """
            Função para salvar os dados no perfil.json quando uma nova conta é criada.
        """
        path: str = os.path.join(self._base_path, 'perfil.json')
        os.makedirs(self._base_path, exist_ok=True)

        with open(path, 'w', encoding = 'utf-8') as js:
            json.dump(self.retorna_dict(), js, indent = 4, ensure_ascii = False)
        self._dirty = True

    def load_profile_json(cls, pasta_base: str) -> dict:
        """
            Função para carregar o perfil.json

        Args:
            pasta_base (str): pasta da conta + perfil.json

        Returns:
            None | dict : nada ou dicionário com os dados do perfil.json
        """
        path: str = os.path.join(pasta_base, "perfil.json")

        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as js:
            return json.load(js)