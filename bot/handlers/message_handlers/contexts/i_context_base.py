from abc import ABC, abstractmethod


class IContextBase(ABC):
    @staticmethod
    @abstractmethod
    def __guard(func) -> callable:
        pass
