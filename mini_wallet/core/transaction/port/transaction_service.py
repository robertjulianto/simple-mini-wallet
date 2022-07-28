from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from mini_wallet.core.auth.port.authentication_service import CustomerContext
from mini_wallet.core.common.enums import TransactionStatus
from mini_wallet.core.common.spec import BaseServiceResult


@dataclass
class CreateTransactionSpec:
    amount: Decimal
    reference_id: str


@dataclass
class CreateTransactionResultData:
    id: str
    status: TransactionStatus
    amount: Decimal
    reference_id: str


@dataclass
class CreateDepositResultDataDeposit(CreateTransactionResultData):
    deposited_by: str
    deposited_at: datetime


@dataclass
class CreateDepositResultData:
    deposit: CreateDepositResultDataDeposit


@dataclass
class CreateDepositResult(BaseServiceResult[CreateDepositResultData]):
    pass


@dataclass
class CreateWithdrawResultDataWithdrawal(CreateTransactionResultData):
    withdrawn_by: str
    withdrawn_at: datetime


@dataclass
class CreateWithdrawResultData:
    withdrawal: CreateWithdrawResultDataWithdrawal


@dataclass
class CreateWithdrawResult(BaseServiceResult[CreateWithdrawResultData]):
    pass


class ITransactionService(ABC):

    @abstractmethod
    def deposit_money(self, spec: CreateTransactionSpec,
                      customer_context: CustomerContext) -> CreateDepositResult:
        raise NotImplementedError

    @abstractmethod
    def withdraw_money(self, spec: CreateTransactionSpec,
                       customer_context: CustomerContext) -> CreateWithdrawResult:
        raise NotImplementedError
