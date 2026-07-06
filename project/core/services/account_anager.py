from project.core.user.models.user import User
from .Controllers.estado_app import EstadoApp
from typing import Optional
from pathlib import Path
import json, os, shutil

class AccountManager:
    
    _current_user: User | None = None
    _ACCOUNTS_JSON_PATH: str = r'Assets\Data\contas.json'

    accounts_cache: dict | None = None


    # leitura contas.json
    @classmethod
    def load_json_accounts(cls):
        """
            Função para carregar o contas.json armazenando os cados em cache (cls.accounts_cache).
        """
        with open(cls._ACCOUNTS_JSON_PATH, 'r', encoding = 'utf-8') as js:
            cls.accounts_cache = json.load(js)

    @classmethod
    def save_accounts_json(cls):
        """
            Salva os dados novos no contas.json (cls.accounts_cache).
        """
        if cls.accounts_cache is None:
            cls.accounts_cache = {'conta_atual' : None, 'contas' : []}
        with open(cls._ACCOUNTS_JSON_PATH, 'w', encoding = 'utf-8') as js:
            json.dump(cls.accounts_cache, js, indent = 4, ensure_ascii = False)

    @classmethod
    def _search_account_index(cls, id_conta : str) -> dict:
        """
            Busca a conta por id específico.

        Args:
            id_conta (str): ID da conta.

        Returns:
            dict : dados da conta.
        """
        if cls.accounts_cache is None:
            cls.load_json_accounts()
        for account in cls.accounts_cache.get('contas', []):
            if account.get('id') == id_conta:
                return account
        return None


    # carregar/instanciar Usuario
    @classmethod
    def load_account(cls, account_id : str, base_path : str, data : dict | None = None):
        """
            Cria Usuario e coloca em memoria. Se 'data' for None ou estiver incompleto, tenta ler perfil.json da base_path.

        Args:
            account_id (str): ID da conta a ser carregada.
            base_path (str): Pasta base da conta
            data (dict | None, optional): Dados retornados ao ler a conta. { Defaults to None }
        """
        
        profile: dict = {}
        
        if data:
            profile.update(data)

        # se faltar alguma chave, tenta carregar do disco
        if not profile.get("nome") or not profile.get("email") or not profile.get("imagem"):
            caminho_perfil = os.path.join(base_path, "perfil.json")
            if os.path.exists(caminho_perfil):
                with open(caminho_perfil, "r", encoding = "utf-8") as f:
                    try:
                        disc = json.load(f)
                        profile.update(disc)
                    except Exception:
                        pass
        
        name: str = profile.get('nome', '')
        email: str = profile.get('email', '')
        image: str = profile.get('imagem', '')

        cls._current_user = User(
            account_id = account_id,
            base_path = base_path,
            name = name,
            email = email,
            image = image
        )

        EstadoApp.notificar('conta_atual', cls._current_user)

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
        if cls._search_account_index(account_id) is not None:
            return False
        
        novo = {'id' : account_id, 'name' : name, 'email' : email, 'pasta_base' : base_path}

        cls.accounts_cache['contas'].append(novo)
        cls.accounts_cache['conta_atual'] = account_id
        cls.save_accounts_json()
        return True
    
    @classmethod
    def update_name_in_index(cls, id_conta : str, novo_nome : str):
        """
            Atualiza o nome específico do usuário (via ft.TextField) no contas.json. 

        Args:
            id_conta (str): ID da conta.
            novo_nome (str): Novo nome de usuário a ser a colocado.

        Returns:
            bool : True se sucedida.
        """
        cls.load_json_accounts()
        
        account: dict = cls._search_account_index(id_conta)

        if not account:
            return False
        
        account['nome'] = novo_nome
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
        
        account: dict = cls._search_account_index(account_id)

        if not account:
            return False
        
        path = account.get('pasta_base')

        # carrega Usuario a partir do perfil.json
        cls.load_account(account_id = account_id, pasta_base = path, dados = account)
        cls.accounts_cache['conta_atual'] = account_id
        cls.save_accounts_json()

        return True
    
    @classmethod
    def read_current_account_index(cls) -> str:
        """
            Função para ler a conta atual logada.

        Returns:
            str : ID da conta atual logada
        """
        cls.load_json_accounts()
        return cls.accounts_cache.get('conta_atual')
    
    @classmethod
    def delete_account(cls, account_id : str):
        """
            Função para excluir a atual conta.
              →  Se não tiver mais contas salvas além da atual: Notifica o EstadoApp por estar 'sem_conta' disponível.
              →  Senão: Exclui a atual conta.

        Args:
            account_id (str) : ID da conta a ser excluído
        """
        cls.load_json_accounts()

        path: str = Path(f"Assets/Data/Contas/{account_id}")
        
        if path.exists():
            shutil.rmtree(path)

        cls.accounts_cache["contas"] = [
            conta for conta in cls.accounts_cache['contas']
            if conta.get('id') != account_id
        ]

        if account_id:
            if cls.accounts_cache.get('contas'):
                other_account = cls.accounts_cache.get('contas')[0]
                
                cls.accounts_cache['conta_atual'] = other_account.get('id')
                cls.save_accounts_json()

                cls.load_account(
                    account_id = other_account.get('id'),
                    pasta_base = other_account.get('pasta_base'),
                    dados = other_account
                )
            else:
                cls.accounts_cache['conta_atual'] = None
                cls._current_user = None
                cls.save_accounts_json()
                EstadoApp.notificar('sem_conta')
        
        EstadoApp.notificar('conta_atual', cls.accounts_cache)