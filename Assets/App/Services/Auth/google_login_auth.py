import aiohttp, os, json
from google_auth_oauthlib.flow import InstalledAppFlow
from Assets.App.Services.gerenciador_contas import GerenciadorContas

def criar_pastas(caminho : str):
    """
        Função para criar as pastas da conta nova.

    Args:
        caminho (str): caminho de cada pasta a ser criada
    """
    os.makedirs(caminho, exist_ok = True)

def criar_jsons(caminho : str, conteudo : dict | None):
    """
        Função para criar os JSONs de cada conta nova.

    Args:
        caminho (str): caminho de cada JSON novo.
    """
    with open(caminho, 'w', encoding = 'utf-8') as js:
        json.dump(conteudo if conteudo is not None else {}, js, indent = 4, ensure_ascii = False)

async def login_google():
    """
        Faz o login via Google OAuth e retorna:
        →  nome
        →  email
        →  foto_perfil (URL)
        →  token (caso precise para People API futuramente)
    """

    SCOPES = [
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    # O fluxo de autenticação OAuth DO GOOGLE NÃO É ASSÍNCRONO
    # então essa parte continua síncrona mesmo (não tem como mudar),
    # mas o resto (requisição da foto) será async.

    flow = InstalledAppFlow.from_client_secrets_file(
        r'Assets\App\Services\Auth\client_secret_google.json',
        scopes = SCOPES
    )

    creds = flow.run_local_server(port=0)

    # Agora buscamos as informações do usuário via chamada async
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {creds.token}'}
        ) as resp:
            dados = await resp.json()

    # Extrair dados retornados
    nome = dados.get('name')
    email = dados.get('email')
    imagem = dados.get('picture')
    id_conta = dados.get("sub")
    pasta_base = f'Assets/Data/Contas/{id_conta}'

    # aumentar qualidade da imagem da conta (trocar s96 por s256)
    if imagem and 's96' in imagem:
        imagem = imagem.replace('s96', 's256')

    dados_user = {'nome': nome, 'email': email, 'imagem': imagem}
    dados_json = {'id' : id_conta, 'nome': nome, 'email': email, 'pasta_base': f'Assets/Data/Contas/{id_conta}'}
    dados_config = {
        "Overlays" : {
            "ON_overlay_dica_tamanho_da_playlist" : True
        }
    }
    dados_play = {
        "ultima_atualizacao" : None,
        "ultimo_id" : 0,
        "playlists" : {}
    }
    caminho_conta = f'Assets/Data/Contas/{id_conta}'

    # geral da conta
    criar_pastas(caminho = caminho_conta)
    criar_jsons(caminho = os.path.join(caminho_conta, 'perfil.json'), conteudo = None)
    criar_jsons(caminho = os.path.join(caminho_conta, 'config.json'), conteudo = dados_config)
    criar_jsons(caminho = os.path.join(caminho_conta, 'playlists.json'), conteudo = dados_play)

    # playlist
    criar_pastas(caminho = os.path.join(caminho_conta, 'Playlists'))

    # estado
    criar_pastas(caminho = os.path.join(caminho_conta, 'Estado'))
    criar_jsons(caminho = os.path.join(caminho_conta, 'Estado/favoritas.json'), conteudo = None) 
    criar_jsons(caminho = os.path.join(caminho_conta, 'Estado/historico.json'), conteudo = None)
    
    # Music e metas
    criar_pastas(caminho = os.path.join(caminho_conta, 'Music'))
    criar_jsons(caminho = os.path.join(caminho_conta, 'Music/letra.json'), conteudo = None)
    criar_jsons(caminho = os.path.join(caminho_conta, 'Music/musicas.json'), conteudo = None)

    # imagens
    criar_pastas(caminho = os.path.join(caminho_conta, 'Imagens'))
    criar_pastas(caminho = os.path.join(caminho_conta, 'Imagens/Capa Musica'))
    criar_pastas(caminho = os.path.join(caminho_conta, 'Imagens/Artistas'))
    criar_pastas(caminho = os.path.join(caminho_conta, 'Imagens/Albuns'))

    GerenciadorContas.carregar_conta(
        id_conta = id_conta,
        pasta_base = pasta_base,
        dados = dados_user
    )
    GerenciadorContas.usuario().salvar()
    GerenciadorContas.adicionar_conta_no_index(id_conta = id_conta, nome = nome, pasta_base = pasta_base, email = email)