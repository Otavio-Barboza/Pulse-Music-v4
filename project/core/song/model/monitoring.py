# import geral
import threading


class Monitoring:

    @classmethod
    def notify_end(cls):
        from core.song.controller.reproduction_manager import ReproductionManager
        ReproductionManager.handle_end_of_music()