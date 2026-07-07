from pathlib import Path
import json

class CreateItens:

    @classmethod
    def create_path(cls, path: Path):
        path.mkdir(exist_ok = True, parents = True)

    @classmethod
    def create_json(cls, path: Path, data: dict):
        if path.exists():
            return
        
        with open(path, 'w', encoding = 'utf-8') as js:
            json.dump(data or {}, js, indent = 4, ensure_ascii = False)

    @classmethod
    def sync_load_json(cls, path, data: dict):
        ...

    @classmethod
    def async_load_json(cls, path, data: dict):
        ...

    @classmethod
    def sync_update_json(cls, path, data: dict):
        ...

    @classmethod
    def async_update_json(cls, path, data: dict):
        ...