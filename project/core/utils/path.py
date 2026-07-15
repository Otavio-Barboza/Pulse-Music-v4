# import de back-end
# from core.services.account_manager import AccountManager
# imports gerais
from pathlib import Path
import os


class AppPaths:

    # assets local
    BASE_DIR = Path(__file__).resolve().parents[2]  # ajuste conforme a localização deste arquivo

    # assets
    ASSETS_JSON: Path = BASE_DIR / "assets" / "auth" / "client_secret_google.json"


    # local app data do windows
    LOCAL_APP_DATA: Path = Path(os.getenv("LOCALAPPDATA")) / "Pulse Music"
    
    # pastas
    ACCOUNT: Path = LOCAL_APP_DATA / "account"
    CONFIG: Path = LOCAL_APP_DATA / "config"
    CACHE: Path = LOCAL_APP_DATA / "cache"

    # jsons
    ACCOUNT_JSON: Path = LOCAL_APP_DATA / "accounts.json"


print(AppPaths.ACCOUNT_JSON)
