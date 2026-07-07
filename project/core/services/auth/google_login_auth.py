from project.core.services.account_manager import AccountManager
from project.core.utils.path import AppPaths
from project.core.utils.utils import CreateItens
from google_auth_oauthlib.flow import InstalledAppFlow
import aiohttp, datetime


async def login_google():
    """
        Faz o login via Google OAuth e retorna:
        →  nome
        →  email
        →  foto_perfil (URL)
        →  token (caso precise para People API futuramente)
    """
    
    # criando (C:\Users\barbo\AppData\Local\Pulse Music\)
    AppPaths.ROOT.mkdir(parents = True, exist_ok = True)

    # criando: (C:\Users\barbo\AppData\Local\Pulse Music\accounts.json)
    CreateItens.create_json(path = AppPaths.ROOT / "accounts.json", data = {})

    # criando: (C:\Users\barbo\AppData\Local\Pulse Music\account\)
    AppPaths.ACCOUNT.mkdir(parents = True, exist_ok = True)


    _SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]

    # O fluxo de autenticação OAuth DO GOOGLE NÃO É ASSÍNCRONO
    # então essa parte continua síncrona mesmo (não tem como mudar),
    # mas o resto (requisição da foto) será async.

    _FLOW = InstalledAppFlow.from_client_secrets_file(
        r'Assets\App\Services\Auth\client_secret_google.json',
        scopes = _SCOPES
    )

    _CREDS = _FLOW.run_local_server(port=0)

    # Agora buscamos as informações do usuário via chamada async
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {_CREDS.token}"}
        ) as resp:
            data = await resp.json()

    # Extrair data retornados
    _name: str = data.get("name")
    _email: str = data.get("email")
    _image: str = data.get("picture")
    _account_id: str = data.get("sub")
    _base_path: str = AppPaths.ACCOUNT / _account_id

    # aumentar qualidade da image da conta (trocar s96 por s256)
    if image and "s96" in image:
        image = image.replace("s96", "s256")


    # criando estrutura dos jsons referentes a conta
    data_profile = {
        "account_id" : _account_id,
        "name": _name, 
        "email": _email, 
        "image": _image
    }
    data_settings = {
        "overlays" : {
            "ON_overlay_playlist_size_tip" : True
        }
    }
    data_playlist = {
        "latest_actualization" : datetime.datetime.now().isoformat(),
        "latest_id" : 0,
        "playlists" : {}
    }


    # caminho da conta agora é: (C:\Users\barbo\AppData\Local\Pulse Music\account)
    AccountManager.create_account_structure(
        base_path = _base_path,
        data_profile = data_profile,
        data_playlist = data_playlist,
        data_settings = data_settings
    )
    AccountManager.load_account(
        account_id = _account_id,
        base_path = _base_path,
        data = data_profile
    )
    AccountManager.user().save_json()
    AccountManager.add_account_to_index(
        account_id = _account_id, 
        name = _name, 
        base_path = _base_path, 
        email = _email
    )