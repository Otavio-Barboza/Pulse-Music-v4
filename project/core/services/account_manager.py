# imports de back-end
from core.user.models.user import User
from core.services.controllers.state_app import StateApp
from core.utils.utils import Utils
from core.utils.path import AppPaths

# imports gerais
from typing import Optional
from pathlib import Path
import json, shutil


class AccountManager:
    
    _current_user: User | None = None
    accounts_cache: dict[str, list[dict]] | None = None


    @classmethod
    def create_account_structure(
        cls, 
        base_path: Path, 
        data_profile: dict[str, str], 
        data_playlist: dict[str, str | int | dict],
        data_settings: dict[str, dict[str, bool]]
    ):
        """
        _summary_: Função para criar toda a estrutura base de pastas e arquivos JSON necessários para operação do aplicativo.

        Args:
            base_path (Path): path base para criação de cada pasta ou arquivo.
            data_profile (dict[str, str]): dados do perfil do usuário.
            data_playlist (dict[str, str  |  int  |  dict]): dados das playlist.
            data_settings (dict[str, dict[str, bool]]): dados de configurações (overlays)
        """
        Utils.create_path(path = base_path)

        # geral da conta
        Utils.create_json(path = base_path / "profile.json", data = data_profile)
        Utils.create_json(path = base_path / "settings.json", data = data_settings)
        Utils.create_json(path = base_path / "playlists.json", data = data_playlist)

        # playlist
        Utils.create_path(path = base_path / "playlists")

        # Music e metas
        Utils.create_path(path = base_path / "music")
        Utils.create_json(path = base_path / "music" / "lyrics.json", data = {})
        Utils.create_json(path = base_path / "music" / "artists.json", data = {})
        Utils.create_json(path = base_path / "music" / "favorites.json", data = {})
        Utils.create_json(path = base_path / "music" / "songs.json", data = {})

        # imagens
        Utils.create_path(path = base_path / "images")
        Utils.create_path(path = base_path / "images" / "covers")
        Utils.create_path(path = base_path / "images" / "albums")
        Utils.create_path(path = base_path / "images" / "artists")


    # leitura e inserção dos dados em contas.json
    @classmethod
    def load_json_accounts(cls) -> bool:
        """
            Função para carregar o accounts.json armazenando os cados em cache (cls.accounts_cache).
        """

        if AppPaths.ACCOUNT_JSON.exists():
            cls.accounts_cache = Utils.sync_load_json(AppPaths.ACCOUNT_JSON)
            return True
        else:
            return False

    @classmethod
    def save_accounts_json(cls):
        """
            Salva os dados novos no accounts.json (cls.accounts_cache).
        """
        if cls.accounts_cache is None:
            cls.accounts_cache = {"current_account" : None, "accounts" : []}

        Utils.sync_update_json(
            path = AppPaths.ACCOUNT_JSON,
            data = cls.accounts_cache
        )

    @classmethod
    def save_profile_json(cls):
        """
            _summary_: Função para atualizar o profile.json com os dados novos após atualização da caixa de texto para o nome novo.
        """

        profile_json = Utils.sync_load_json(
            AppPaths.ACCOUNT / cls.accounts_cache["current_account"] / "profile.json"
        )

        profile_json["name"] = cls.user().name
        Utils.sync_update_json(
            path = AppPaths.ACCOUNT / cls.accounts_cache["current_account"] / "profile.json",
            data = profile_json
        )

    @classmethod
    def search_account_index(cls, account_id: str) -> dict:
        """
            Busca a conta por id específico.

        Args:
            account_id (str): ID da conta.

        Returns:
            dict : dados da conta.
        """

        if cls.accounts_cache is None:
            cls.load_json_accounts()
        for account in cls.accounts_cache.get("accounts", []):
            if account.get("id") == account_id:
                return account
        return None


    # carregar/instanciar Usuario
    @classmethod
    def load_account(cls, account_id: str, base_path: Path, data: dict | None = None):
        """
            Cria Usuario e coloca em memoria. Se 'data' for None ou estiver incompleto, tenta ler perfil.json da base_path.

        Args:
            account_id (str): ID da conta a ser carregada.
            base_path (str): Pasta base da conta
            data (dict | None, optional): Dados retornados ao ler a conta. { Defaults to None }
        """

        cls._current_user = User(
            account_id = account_id,
            base_path = base_path,
            name = data.get("name"),
            email = data.get("email"),
            image = data.get("image")
        )


    @classmethod
    def user(cls) -> User:
        """
            Função para acessar dados, atributos, funções de Usuario por AccountManager.

        Returns:
            Usuario : atributos ou funções da classe Usuario
        """
        return cls._current_user
    
    # operações do index: adicionar, atualizar nome, selecionar
    @classmethod
    def add_account_to_index(cls, account_id : str, name : str, base_path : str, email : str):
        """
            Adiciona uma conta nova no indice de contas.json 

        Args:
            account_id (str): ID da conta a ser adicionada.
            name (str): Nome do usuário.
            base_path (str): Pasta base para adicionar a conta.
            email (str): Email da conta do usuário a ser adicionado.

        Returns:
            bool : True se sucedida.
        """

        cls.load_json_accounts()
        
        if cls.search_account_index(account_id) is not None:
            return False
        
        novo = {
            "id" : account_id, 
            "name" : name, 
            "email" : email, 
            "base_path" : str(base_path) #transformando em string para salvar no JSON
        }

        # adicionando uma nova conta a lista de contas do cache
        cls.accounts_cache["accounts"].append(novo)
        cls.accounts_cache["current_account"] = account_id
        
        cls.save_accounts_json()
        cls.save_profile_json()
        
    @classmethod
    def update_name_in_index(cls, account_id: str, new_name: str):
        """
            atualiza o nome do usuário no accounts.json

        Args:
            id_conta (str): ID da conta.
            new_name (str): Novo nome de usuário a ser a colocado.

        Returns:
            bool : True se sucedida.
        """
        cls.load_json_accounts()
        
        accounts: dict = cls.search_account_index(account_id)

        if not accounts:
            return False
        
        accounts["name"] = new_name
        cls.save_accounts_json()

        return True
    
    @classmethod
    def select_account_by_id(cls, account_id : str):
        """
            Função para selecionar uma conta por um ID específico.

        Args:
            account_id (str): ID da conta a ser selecionada.

        Returns:
            bool : True se sucedida.
        """
        cls.load_json_accounts()
        
        accounts: dict = cls.search_account_index(account_id)
        
        if not accounts:
            return False
        
        profile_json = Utils.sync_load_json(
            AppPaths.ACCOUNT / account_id / "profile.json"
        )

        # carrega Usuario a partir do perfil.json
        cls.load_account(account_id = account_id, base_path = accounts.get("base_path"), data = profile_json)
        cls.accounts_cache["current_account"] = account_id
        cls.save_accounts_json()

        return True
    
    @classmethod
    def read_current_account_index(cls) -> str | None:
        """
            Função para ler a conta atual logada.

        Returns:
            str : ID da conta atual logada
        """
        if cls.load_json_accounts():
            return cls.accounts_cache.get("current_account")
        else:
            return None
        
    @classmethod
    async def delete_account(cls, page, account_id: str):
        """
            Função para excluir a atual conta.
              →  Se não tiver mais contas salvas além da atual: Notifica o StateApp por estar 'sem_conta' disponível.
              →  Senão: Exclui a atual conta.

        Args:
            account_id (str) : ID da conta a ser excluído
        """
        cls.load_json_accounts()

        path: Path = AppPaths.ACCOUNT / account_id
        
        if path.exists():
            shutil.rmtree(path)

        cls.accounts_cache["accounts"] = [
            conta for conta in cls.accounts_cache["accounts"]
            if conta.get("id") != account_id
        ]
        
        if account_id:
            if cls.accounts_cache.get("accounts"):
                other_account = cls.accounts_cache.get("accounts")[0]
                account_profile = Utils.sync_load_json(
                    AppPaths.ACCOUNT / other_account.get("id") / "profile.json"
                )

                cls.accounts_cache["current_account"] = other_account.get("id")
                cls.save_accounts_json()

                cls.load_account(
                    account_id = other_account.get("id"),
                    base_path = other_account.get("base_path"),
                    data = account_profile
                )
            else:
                cls.accounts_cache["current_account"] = None
                cls._current_user = None
                cls.save_accounts_json()
                
                from core.services.auth.google_login_auth import login_google
                import asyncio

                await login_google(page)