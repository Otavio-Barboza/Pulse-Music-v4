from pathlib import Path
import os

class AppPaths:

    # assets local
    LOCAL_ASSETS: Path = "project"

    # assets
    ASSETS: Path = LOCAL_ASSETS / "assets" / "auth"


    # local app data do windows
    LOCAL_APP_DATA: Path = Path(os.getenv("LOCALAPPDATA")) / "Pulse Music"
    
    # pastas
    ACCOUNT: Path = LOCAL_APP_DATA / "account"
    CONFIG: Path = LOCAL_APP_DATA / "config"
    CACHE: Path = LOCAL_APP_DATA / "cache"

    # jsons
    ACCOUNT_JSON: Path = LOCAL_APP_DATA / "accounts.json"


print(AppPaths.LOCAL_APP_DATA)
print(AppPaths.ACCOUNT)
print(AppPaths.CONFIG)
print(AppPaths.CACHE)