from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from mini_wallet.core.common.enums import WalletStatus


@dataclass
class BaseWalletAccessorSpec:
    id: str


@dataclass
class BaseWalletAccessorResult(BaseWalletAccessorSpec):
    owner_id: str
    status: WalletStatus
    enabled_at: Optional[datetime] = None
    disabled_at: Optional[datetime] = None


@dataclass
class CreateWalletAccessorSpec:
    owner_id: str
    token: str


@dataclass
class CreateWalletAccessorResult(BaseWalletAccessorSpec):
    pass


@dataclass
class UpdateWalletStatusAccessorSpec(BaseWalletAccessorSpec):
    status: WalletStatus
    enabled_at: Optional[datetime] = None
    disabled_at: Optional[datetime] = None


@dataclass
class UpdateWalletStatusAccessorResult(BaseWalletAccessorResult):
    pass


@dataclass
class GetWalletByIdAccessorSpec(BaseWalletAccessorSpec):
    pass


@dataclass
class GetWalletByIdAccessorResult(BaseWalletAccessorResult):
    pass


@dataclass
class GetWalletByTokenAccessorSpec:
    token: str


@dataclass
class GetWalletByTokenAccessorResult(BaseWalletAccessorResult):
    pass


class IWalletAccessor(ABC):

    @abstractmethod
    def create_wallet(self, accessor_spec: CreateWalletAccessorSpec) -> CreateWalletAccessorResult:
        raise NotImplementedError

    @abstractmethod
    def update_wallet_status(self, accessor_spec: UpdateWalletStatusAccessorSpec) -> UpdateWalletStatusAccessorResult:
        raise NotImplementedError

    @abstractmethod
    def get_wallet_by_id(self, accessor_spec: GetWalletByIdAccessorSpec) -> GetWalletByIdAccessorResult:
        raise NotImplementedError

    @abstractmethod
    def get_wallet_by_token(self, accessor_spec: GetWalletByTokenAccessorSpec) -> GetWalletByTokenAccessorResult:
        raise NotImplementedError
