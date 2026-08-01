# import geral
import aiohttp


class Network:
    def __init__(self):
        self.session = None

    async def initialize(self):
        self.session = aiohttp.ClientSession()

    async def has_internet(self):
        try:
            async with self.session.get(
                "https://clients3.google.com/generate_204",
                timeout = 3,
            ):
                return True
        except (aiohttp.ClientError, TimeoutError):
            return False

    async def close(self):
        await self.session.close()

network = Network()