from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class GetBalanceByWalletIdSpec:
    wallet_id: str


@dataclass
class GetBalanceByWalletIdResult:
    balance_amount: Decimal


class IBalanceService(ABC):

    @abstractmethod
    def get_balance_by_wallet_id(self, spec: GetBalanceByWalletIdSpec) -> GetBalanceByWalletIdResult:
        raise NotImplementedError
