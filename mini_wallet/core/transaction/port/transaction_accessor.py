from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from mini_wallet.core.common.enums import TransactionStatus, TransactionType


@dataclass
class CreateTransactionAccessorSpec:
    wallet_id: str
    amount: Decimal
    reference_id: str
    type: TransactionType
    status: TransactionStatus


@dataclass
class BaseTransactionAccessorResult:
    id: str
    wallet_id: str
    status: TransactionStatus
    transaction_time: datetime
    amount: Decimal
    reference_id: str
    type: TransactionType


@dataclass
class CreateTransactionAccessorResult(BaseTransactionAccessorResult):
    pass


@dataclass
class GetTransactionByWalletIdSpec:
    wallet_id: str


@dataclass
class GetTransactionsByWalletIdResult:
    transactions: List[BaseTransactionAccessorResult]


@dataclass
class GetTransactionByReferenceIdSpec:
    reference_id: str


@dataclass
class GetTransactionByReferenceIdResult:
    transaction_id: Optional[str]


class ITransactionAccessor(ABC):

    @abstractmethod
    def create_transaction(self, accessor_spec: CreateTransactionAccessorSpec) -> CreateTransactionAccessorResult:
        raise NotImplementedError

    @abstractmethod
    def get_transactions_by_wallet_id(
            self, accessor_spec: GetTransactionByWalletIdSpec) -> GetTransactionsByWalletIdResult:
        raise NotImplementedError

    @abstractmethod
    def get_transactions_by_reference_id(
            self, accessor_spec: GetTransactionByReferenceIdSpec) -> GetTransactionByReferenceIdResult:
        raise NotImplementedError
