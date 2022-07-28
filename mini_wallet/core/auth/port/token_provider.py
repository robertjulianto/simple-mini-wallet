from abc import ABC, abstractmethod


class ITokenProvider(ABC):
    @abstractmethod
    def generate_token(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        raise NotImplementedError
