# imports gerais
import inspect, asyncio


class StateApp:
    current_account = None
    open_settings = False
    current_configuration_session = None
    overlay_tips = True
    _callbacks = {}

    @classmethod
    def register_callback(cls, event: str, func : callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(func)

    @classmethod
    def notify(cls, event: str, data = None):
        """
            Notifica todos os ouvintes; suporta funções sync e async.
        """

        if event not in cls._callbacks:
            return
        for func in cls._callbacks[event]:
            try:
                if inspect.iscoroutinefunction(func):
                    # listener async
                    asyncio.create_task(func(data))
                else:
                    # pode retornar coroutine (função normal que retorna coroutine)
                    res = func(data)
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception:
                # nunca quebrar a notificação inteira por um erro de listener
                pass

    @classmethod
    def select_config_section(cls, section_name: str):
        # Botão na seção configurações do menu
        cls.current_configuration_session = section_name
        cls.notify("secao_config", section_name)

    @classmethod
    def open_configurations(cls):
        cls.open_settings = True
        cls.notify("open_settings", True)

    @classmethod
    def close_configurations(cls):
        cls.open_settings = False
        cls.notify("open_settings", False)

    @classmethod
    async def set_account(cls, account):
        """
            Atualiza a account atual e notifica todos que dependem dela.
        """

        cls.current_account = account

        for fuction in cls._callbacks['current_account']:
            r = fuction(account)
            if hasattr(r, '__await__'):
                await r