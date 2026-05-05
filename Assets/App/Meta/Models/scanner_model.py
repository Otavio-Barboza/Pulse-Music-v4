from ..Controller.status import StatusScanner
from ..Repository.persistencia import Persistencia
from ...Services.gerenciador_contas import GerenciadorContas
from ..Scanner.scanner import Scanner
import asyncio, os

class ScannerModel:
    _tupla_status = (
        StatusScanner.ON, StatusScanner.PAUSE, StatusScanner.BREAK, 
        StatusScanner.ON_SCANNER, StatusScanner.ON_PIPELINE_PLAYLIST
    )
    _status_operacao = StatusScanner.ON
    _status_processos = None
    _tarefas_ativas = 0
    
    @classmethod
    async def _async_iniciar_scanner(cls):
        cls.alterar_status(
            None
        )
        Scanner.gerenciar_status()
        
        while cls._status_operacao != StatusScanner.BREAK:
            if cls._status_operacao == StatusScanner.PAUSE:
                await asyncio.sleep(1)
            else:
                await Scanner._async_verificar_json()
                await asyncio.sleep(5)
        else:
            raise('Scanner parou inesperadamente!')

    @classmethod
    def alterar_status(cls, status : StatusScanner):
        for stt in cls._tupla_status:
            if stt == status:
                cls.status = stt
                break
            
    @classmethod
    def definir_status_processo(cls, status : StatusScanner | None = None):
        cls._status_processos = status
    
    @classmethod
    def iniciar_tarefa(cls):
        cls._tarefas_ativas += 1

    @classmethod
    def finalizar_tarefa(cls):
        cls._tarefas_ativas -= 1

    @classmethod
    def esta_ocupado(cls):
        return cls._tarefas_ativas > 0