# imports gerais
from pathlib import Path
import json, aiofiles


class Utils:

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
    def sync_load_json(cls, path: Path) -> dict:
        with open(path, 'r', encoding = 'utf-8') as js:
            return json.load(js)

    @classmethod
    def sync_update_json(cls, path, data: dict):
        with open(path, 'w', encoding = 'utf-8') as js:
            json.dump(data or {}, js, indent = 4, ensure_ascii = False)

    @classmethod
    async def async_load_json(cls, path: Path):
        async with aiofiles.open(path, 'r', encoding = 'utf-8') as j:
            return json.loads(await j.read())

    @classmethod
    async def async_update_json(cls, path: Path, data: dict):
        async with aiofiles.open(path, 'w', encoding = 'utf-8') as j:
            content = json.dumps(
                data,
                ensure_ascii = False,
                indent = 4
            )
            await j.write(content)