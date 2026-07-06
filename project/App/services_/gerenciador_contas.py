from ..Usuario.Models.usuario import Usuario
from .Controllers.estado_app import EstadoApp
from typing import Optional
from pathlib import Path
import json, os, shutil

class GerenciadorContas:
    usuario_atual : Usuario | None = None
    contas_cache : dict | None = None
    CAMINHO_CONTAS_JSON = r'Assets\Data\contas.json'

    # leitura contas.json
    @classmethod
    def carregar_contas_json(cls):
        """
            Função para carregar o contas.json armazenando os cados em cache (cls.contas_cache).
        """
        with open(cls.CAMINHO_CONTAS_JSON, 'r', encoding = 'utf-8') as js:
            cls.contas_cache = json.load(js)

    @classmethod
    def salvar_contas_json(cls):
        """
            Salva os dados novos no contas.json (cls.contas_cache).
        """
        if cls.contas_cache is None:
            cls.contas_cache = {'conta_atual' : None, 'contas' : []}
        with open(cls.CAMINHO_CONTAS_JSON, 'w', encoding = 'utf-8') as js:
            json.dump(cls.contas_cache, js, indent = 4, ensure_ascii = False)

    @classmethod
    def _buscar_conta_index(cls, id_conta : str) -> dict:
        """
            Busca a conta por id específico.

        Args:
            id_conta (str): ID da conta.

        Returns:
            dict : dados da conta.
        """
        if cls.contas_cache is None:
            cls.carregar_contas_json()
        for conta in cls.contas_cache.get('contas', []):
            if conta.get('id') == id_conta:
                return conta
        return None


    # carregar/instanciar Usuario
    @classmethod
    def carregar_conta(cls, id_conta : str, pasta_base : str, dados : dict | None = None):
        """
            Cria Usuario e coloca em memoria. Se 'dados' for None ou estiver incompleto, tenta ler perfil.json da pasta_base.

        Args:
            id_conta (str): ID da conta a ser carregada.
            pasta_base (str): Pasta base da conta
            dados (dict | None, optional): Dados retornados ao ler a conta. { Defaults to None }
        """
        perfil = {}
        if dados:
            perfil.update(dados)

        # se faltar alguma chave, tenta carregar do disco
        if not perfil.get("nome") or not perfil.get("email") or not perfil.get("imagem"):
            caminho_perfil = os.path.join(pasta_base, "perfil.json")
            if os.path.exists(caminho_perfil):
                with open(caminho_perfil, "r", encoding="utf-8") as f:
                    try:
                        disco = json.load(f)
                        perfil.update(disco)
                    except Exception:
                        pass
        
        nome = perfil.get('nome', '')
        email = perfil.get('email', '')
        imagem = perfil.get('imagem', '')

        cls.usuario_atual = Usuario(
            id_conta = id_conta,
            pasta_base = pasta_base,
            nome = nome,
            email = email,
            imagem = imagem
        )

        EstadoApp.notificar('conta_atual', cls.usuario_atual)

    @classmethod
    def usuario(cls) -> Usuario:
        """
            Função para acessar dados, atributos, funções de Usuario por GerenciadorContas.

        Returns:
            Usuario : atributos ou funções da classe Usuario
        """
        return cls.usuario_atual
    
    # operações do index: adicionar, atualizar nome, selecionar
    @classmethod
    def adicionar_conta_no_index(cls, id_conta : str, nome : str, pasta_base : str, email : str):
        """
            Adiciona uma conta nova no indice de contas.json 

        Args:
            id_conta (str): ID da conta a ser adicionada.
            nome (str): Nome do usuário.
            pasta_base (str): Pasta base para adicionar a conta.
            email (str): Email da conta do usuário a ser adicionado.

        Returns:
            bool : True se sucedida.
        """
        cls.carregar_contas_json()
        if cls._buscar_conta_index(id_conta) is not None:
            return False
        
        novo = {'id' : id_conta, 'nome' : nome, 'email' : email, 'pasta_base' : pasta_base}

        cls.contas_cache['contas'].append(novo)
        cls.contas_cache['conta_atual'] = id_conta
        cls.salvar_contas_json()
        return True
    
    @classmethod
    def atualizar_nome_no_index(cls, id_conta : str, novo_nome : str):
        """
            Atualiza o nome específico do usuário (via ft.TextField) no contas.json. 

        Args:
            id_conta (str): ID da conta.
            novo_nome (str): Novo nome de usuário a ser a colocado.

        Returns:
            bool : True se sucedida.
        """
        cls.carregar_contas_json()
        conta = cls._buscar_conta_index(id_conta)

        if not conta:
            return False
        
        conta['nome'] = novo_nome
        cls.salvar_contas_json()
        return True
    
    @classmethod
    def selecionar_conta_por_id(cls, id_conta : str):
        """
            Função para selecionar uma conta por um ID específico.

        Args:
            id_conta (str): ID da conta a ser selecionada.

        Returns:
            bool : True se sucedida.
        """
        cls.carregar_contas_json()
        conta = cls._buscar_conta_index(id_conta)

        if not conta:
            return False
        
        pasta = conta.get('pasta_base')

        # carrega Usuario a partir do perfil.json
        cls.carregar_conta(id_conta = id_conta, pasta_base = pasta, dados = conta)
        cls.contas_cache['conta_atual'] = id_conta
        cls.salvar_contas_json()

        return True
    
    @classmethod
    def ler_conta_atual_index(cls) -> str:
        """
            Função para ler a conta atual logada.

        Returns:
            str : ID da conta atual logada
        """
        cls.carregar_contas_json()
        return cls.contas_cache.get('conta_atual')
    
    @classmethod
    def excluir_conta(cls, id_conta : str):
        """
            Função para excluir a atual conta.
              →  Se não tiver mais contas salvas além da atual: Notifica o EstadoApp por estar 'sem_conta' disponível.
              →  Senão: Exclui a atual conta.

        Args:
            id_conta (str) : ID da conta a ser excluído
        """
        cls.carregar_contas_json()

        pasta = Path(f"Assets/Data/Contas/{id_conta}")
        if pasta.exists():
            shutil.rmtree(pasta)

        cls.contas_cache["contas"] = [
            conta for conta in cls.contas_cache['contas']
            if conta.get('id') != id_conta
        ]

        id_atual = cls.contas_cache.get('conta_atual') == id_conta

        if id_conta:
            if cls.contas_cache.get('contas'):
                nova = cls.contas_cache.get('contas')[0]
                cls.contas_cache['conta_atual'] = nova.get('id')
                cls.salvar_contas_json()

                cls.carregar_conta(
                    id_conta = nova.get('id'),
                    pasta_base = nova.get('pasta_base'),
                    dados = nova
                )
            else:
                cls.contas_cache['conta_atual'] = None
                cls.usuario_atual = None
                cls.salvar_contas_json()
                EstadoApp.notificar('sem_conta')
        
        EstadoApp.notificar('conta_atual', cls.contas_cache)