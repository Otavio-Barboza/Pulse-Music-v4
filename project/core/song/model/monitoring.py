# import de back-end
from project.core.song.controller.reproduction_manager import ReproductionManager

# import geral
import threading


class Monitoring:

    @classmethod
    def notify_end(cls):
        ReproductionManager.handle_end_of_music()