# import de back-end
from core.utils.utils import Utils
from core.utils.path import AppPaths

# imports gerais
from pathlib import Path
import os, json


""" _summary_: 
        - Classe User para ser o modelo de usuário, respoinsabilidade dela é para armazenar os dados e ser o molde do usuário no player. 
        - Responsabilidade de gravar json, atualizar dados, remover dados será centralizada em AccountManager.
"""


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
    
    # carregar
    def to_dict(self) -> dict[str, str]:
        return {
            'id' : self._account_id,
            'name' : self._name,
            "email" : self._email,
            "image" : self._image
        }