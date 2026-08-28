# import geral
import asyncio, threading


class AsyncManager:

    loop = asyncio.new_event_loop()

    @classmethod
    def start(cls):
        threading.Thread(
            target = cls.loop.run_forever,
            daemon = True
        ).start()

    @classmethod
    def create_task(cls, coroutine):
        asyncio.run_coroutine_threadsafe(
            coroutine,
            cls.loop
        )