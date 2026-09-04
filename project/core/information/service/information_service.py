# import de back-end
from core.information.process.information_process import InformationProcess


class InformationService:

    _callbacks: dict[str, list[callable]] = {}


    @classmethod
    def register_callback_event(cls, event: str, callback: callable):
        if event not in cls._callbacks:
            cls._callbacks[event] = []
        cls._callbacks[event].append(callback)

    @classmethod
    def notify_callback_event(cls, event: str):
        for callback in cls._callbacks[event]:
            callback()


    @classmethod
    def get(cls, key: str):
        response = InformationProcess.send({
            "action" : "get",
            "key" : key
        })

        print(f"[INFORMATION SERVICE] Response: {response}")
        print(f"[INFORMATION SERVICE] Response: {response}")
        print(f"[INFORMATION SERVICE] Success: {response.get('success')}")
        print(f"[INFORMATION SERVICE] Not success: {not response.get('success')}")

        if not isinstance(response, dict):
            raise RuntimeError(
                "Resposta inválida do information_main.exe"
            )

        if not response.get("success"):
            raise RuntimeError(
                response.get(
                    "error",
                    "Erro desconhecido ao obter informação."
                )
            )

        return response.get("value")