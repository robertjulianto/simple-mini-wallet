from abc import ABC, abstractmethod
from typing import Optional


class ILogger(ABC):
    @abstractmethod
    def info(self, msg: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def warn(self, msg: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, msg: str, exception: Optional[Exception] = None, extra: dict = None) -> None:
        raise NotImplementedError
