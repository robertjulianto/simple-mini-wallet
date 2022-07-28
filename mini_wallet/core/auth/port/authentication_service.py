from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class AuthenticateSpec:
    customer_xid: str
    wallet_id: str


@dataclass
class GenerateTokenResult:
    token: str


@dataclass
class CustomerContext:
    customer_xid: str
    wallet_id: str


class IAuthenticationService(ABC):

    @abstractmethod
    def generate_token(self) -> GenerateTokenResult:
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str) -> CustomerContext:
        raise NotImplementedError
