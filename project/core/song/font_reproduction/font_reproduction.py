# import geral
from abc import ABC, abstractmethod


class ReproductionFont(ABC):

    @abstractmethod
    def load(self) -> list:
        pass