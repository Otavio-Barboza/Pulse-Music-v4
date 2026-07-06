import inspect, asyncio

class EstadoApp:
    conta_atual = None
    config_aberta = False
    secao_config_atual = None
    overlay_dicas = True
    _ouvintes = {}

    @classmethod
    def registrar_ouvinte(cls, evento: str, func : callable):
        if evento not in cls._ouvintes:
            cls._ouvintes[evento] = []
        cls._ouvintes[evento].append(func)

    @classmethod
    def notificar(cls, evento: str, dados=None):
        """
            Notifica todos os ouvintes; suporta funções sync e async.
        """
        if evento not in cls._ouvintes:
            return
        for func in cls._ouvintes[evento]:
            try:
                if inspect.iscoroutinefunction(func):
                    # listener async
                    asyncio.create_task(func(dados))
                else:
                    # pode retornar coroutine (função normal que retorna coroutine)
                    res = func(dados)
                    if inspect.isawaitable(res):
                        asyncio.create_task(res)
            except Exception:
                # nunca quebrar a notificação inteira por um erro de listener
                pass

    @classmethod
    def selecionar_secao_config(cls, nome_secao):
        # Botão na seção configurações do menu
        cls.secao_config_atual = nome_secao
        cls.notificar("secao_config", nome_secao)

    @classmethod
    def abrir_config(cls):
        cls.config_aberta = True
        cls.notificar("config_aberta", True)

    @classmethod
    def fechar_config(cls):
        cls.config_aberta = False
        cls.notificar("config_aberta", False)

    @classmethod
    async def set_conta(cls, conta):
        """
            Atualiza a conta atual e notifica todos que dependem dela.
        """

        cls.conta_atual = conta

        for funcao in cls._ouvintes['conta_atual']:
            r = funcao(conta)
            if hasattr(r, '__await__'):
                await r