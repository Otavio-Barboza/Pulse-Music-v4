# import de back-end
from core.network.network import network

# import de front end
from ui.utils.utils_ui import UtilsUi

# import geral
import aiohttp, asyncio, flet, time


class Connection:

    _is_online: bool = False
    _is_connected: bool = False
    _warning_count: int = 0


    @classmethod
    def is_connected(cls) -> bool:
        return cls._is_connected

    @classmethod
    def is_online(cls) -> bool:
        return cls._is_online


    @classmethod
    def set_is_online(cls, value: bool):
        cls._is_online = value

    @classmethod
    def set_is_connected(cls, value: bool):
        cls._is_connected = value


    @classmethod
    async def verify_connection(cls, page: flet.Page):
        connection: bool = await network.has_internet()

        cls.set_is_connected(connection)

        if not cls.is_connected():
            
            if cls._warning_count >= 1:
                return
            
            UtilsUi.snack_bar(
                text = "Você está offline. Alguns recursos não estarão disponíveis.",
                page = page
            ) 
            cls._warning_count += 1

            UtilsUi.connection_app_bar(
                value = True, page = page
            )
        else:

            if cls._warning_count != 0:
                cls._warning_count = 0

                UtilsUi.snack_bar(
                    text = "Conexão retomada, use com moderação...", 
                    page = page
                ) 

                UtilsUi.connection_app_bar(
                    value = False, page = page
                )
            else:
                return
            

    @classmethod
    async def start_loop_connection(cls, page: flet.Page):

        if network.session is None:
            await network.initialize()

        cls.set_is_online(True)

        while True:

            if not cls._is_online:
                return
            
            await cls.verify_connection(page)
            await asyncio.sleep(10)