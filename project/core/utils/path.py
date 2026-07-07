from pathlib import Path
import os

class AppPaths:

    ROOT = Path(os.getenv("LOCALAPPDATA")) / "Pulse Music"
    
    # pastas
    ACCOUNT = ROOT / "account"

    CONFIG = ROOT / "config"

    CACHE = ROOT / "cache"

    # jsons
    ACCOUNT_JSON = ROOT / "accounts.json"


print(AppPaths.ROOT)
print(AppPaths.ACCOUNT)
print(AppPaths.CONFIG)
print(AppPaths.CACHE)