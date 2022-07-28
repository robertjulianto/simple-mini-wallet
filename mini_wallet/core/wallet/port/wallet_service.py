from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from mini_wallet.core.common.enums import WalletStatus
from mini_wallet.core.common.spec import BaseServiceResult


@dataclass
class BaseWalletSpec:
    wallet_id: str


@dataclass
class CreateWalletSpec:
    customer_xid: str


@dataclass
class CreateWalletResultData:
    token: str


@dataclass
class CreateWalletResult(BaseServiceResult[CreateWalletResultData]):
    pass


@dataclass
class EnableWalletSpec(BaseWalletSpec):
    pass


@dataclass
class WalletData:
    id: str
    owned_by: str
    status: WalletStatus
    balance: Decimal


@dataclass
class EnabledWalletData(WalletData):
    enabled_at: datetime


@dataclass
class EnabledWalletResultData:
    wallet: EnabledWalletData


@dataclass
class EnableWalletResult(BaseServiceResult[EnabledWalletResultData]):
    pass


@dataclass
class ViewWalletSpec(BaseWalletSpec):
    pass


@dataclass
class ViewWalletResult(BaseServiceResult[EnabledWalletResultData]):
    pass


@dataclass
class DisableWalletSpec(BaseWalletSpec):
    pass


@dataclass
class DisabledWalletData(WalletData):
    disabled_at: datetime


@dataclass
class DisabledWalletResultData:
    wallet: DisabledWalletData


@dataclass
class DisableWalletResult(BaseServiceResult[DisabledWalletResultData]):
    pass


class IWalletService(ABC):

    @abstractmethod
    def create_wallet(self, spec: CreateWalletSpec) -> CreateWalletResult:
        raise NotImplementedError

    @abstractmethod
    def enable_wallet(self, spec: EnableWalletSpec) -> EnableWalletResult:
        raise NotImplementedError

    @abstractmethod
    def view_wallet(self, spec: ViewWalletSpec) -> ViewWalletResult:
        raise NotImplementedError

    @abstractmethod
    def disable_wallet(self, spec: DisableWalletSpec) -> DisableWalletResult:
        raise NotImplementedError

    @abstractmethod
    def validate_if_wallet_is_enabled(self, wallet_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def validate_if_wallet_is_disabled(self, wallet_id: str) -> None:
        raise NotImplementedError
