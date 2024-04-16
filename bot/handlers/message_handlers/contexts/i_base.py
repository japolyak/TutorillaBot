from abc import ABC, abstractmethod


class IBase(ABC):
    @staticmethod
    @abstractmethod
    def __guard(func) -> callable:
        pass
