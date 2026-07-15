# import de back-end
from project.core.meta.enum.status import ScannerStatus
from project.core.meta.scanner.scanner import Scanner

# imports gerais
import asyncio, os


class ScannerModel:

    status: ScannerStatus | None = None
    _status: tuple[ScannerStatus] = (
        ScannerStatus.ON, ScannerStatus.PAUSE, ScannerStatus.BREAK, 
        ScannerStatus.ON_SCANNER, ScannerStatus.ON_PIPELINE_PLAYLIST
    )
    _status_operation: ScannerStatus = ScannerStatus.ON
    status_procesesses: ScannerStatus | None = None
    _number_of_active_taks: int = 0
    
    @classmethod
    async def async_start_scanner(cls):
        cls.set_status(
            None
        )
        Scanner.gerenciar_status()
        
        while cls._status_operation != ScannerStatus.BREAK:
            if cls._status_operation == ScannerStatus.PAUSE:
                await asyncio.sleep(1)
            else:
                await Scanner._async_verificar_json()
                await asyncio.sleep(5)
        else:
            raise('Scanner parou inesperadamente!')

    @classmethod
    def set_status(cls, status: ScannerStatus):
        for stt in cls._status:
            if stt == status:
                cls.status = stt
                break
            
    @classmethod
    def set_status_prosesses(cls, status: ScannerStatus | None = None):
        cls.status_procesesses = status
    
    @classmethod
    def start_task(cls):
        cls._number_of_active_taks += 1

    @classmethod
    def finaly_task(cls):
        cls._number_of_active_taks -= 1

    @classmethod
    def return_is_busy(cls):
        return cls._number_of_active_taks > 0