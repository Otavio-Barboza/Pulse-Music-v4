# import de back-end
from core.utils.utils import Utils
from core.utils.path import AppPaths

# imports gerais
from pathlib import Path
import os, json


class User:

    def __init__(self, account_id: str, base_path: Path, name: str, email: str, image: str):
        self._account_id = account_id
        self._base_path = base_path
        self._name = name
        self._email = email
        self._image = image
        self._callbacks = []


    # properties (encapsulamento)
    @property
    def id(self) -> str:
        return self._account_id
    
    @property
    def base_path(self) -> Path:
        return self._base_path
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, valor: str):
        if valor is None:
            return
        
        if valor != self._name:
            self._name = valor
            # self.notify_callbacks()

    @property
    def email(self) -> str:
        return self._email
    
    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, valor: str):
        if valor is None:
            return
        
        if valor != self._image:
            self._image = valor
            # self.notify_callbacks()
    

    # callbacks
    def register_callback(self, func: callable):
        if callable(func):
            self._callbacks.append(func)

    def notify_callbacks(self):
        for func in self._callbacks:
            try:
                func(self)
            except Exception:
                pass
    
    
    # carregar
    def to_dict(self) -> dict[str, str]:
        return {
            'id' : self._account_id,
            'name' : self._name,
            "email" : self._email,
            "image" : self._image
        }

    # def save_json(self):
    #     """
    #         Função para salvar os dados no profile.json quando uma nova conta é criada.
    #     """
    #     path: str = os.path.join(self._base_path, 'profile.json')

    #     Utils.sync_update_json(path = self._base_path / "profile.json", data = self.to_dict())
        
    #     self._dirty = True

    def load_profile_json(cls, base_path: str) -> dict:
        """
            Função para carregar o profile.json

        Args:
            base_path (str): pasta da conta + profile.json

        Returns:
            None | dict : nada ou dicionário com os dados do profile.json
        """
        path: str = os.path.join(base_path, "profile.json")

        if not os.path.exists(path):
            return None
        with open(path, "r", encoding = "utf-8") as js:
            return json.load(js)