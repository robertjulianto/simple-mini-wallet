from datetime import timezone, datetime
from decimal import Decimal

from injector import inject

from mini_wallet.core.auth.port.authentication_service import CustomerContext
from mini_wallet.core.balance.port.balance_service import IBalanceService, GetBalanceByWalletIdSpec
from mini_wallet.core.common.enums import ResponseStatus, TransactionType, TransactionStatus
from mini_wallet.core.common.exceptions import TransactionReferenceIsExistsException
from mini_wallet.core.transaction.port.transaction_accessor import ITransactionAccessor, CreateTransactionAccessorSpec, \
    CreateTransactionAccessorResult, GetTransactionByReferenceIdSpec
from mini_wallet.core.transaction.port.transaction_service import ITransactionService, CreateTransactionSpec, \
    CreateDepositResult, \
    CreateDepositResultData, CreateDepositResultDataDeposit, CreateWithdrawResult, \
    CreateWithdrawResultData, CreateWithdrawResultDataWithdrawal
from mini_wallet.core.wallet.port.wallet_accessor import IWalletAccessor, GetWalletByIdAccessorSpec
from mini_wallet.core.wallet.port.wallet_service import IWalletService


class CreateWithdrawResultDataDeposit:
    pass


class TransactionService(ITransactionService):

    @inject
    def __init__(
            self,
            balance_service: IBalanceService,
            wallet_service: IWalletService,
            transaction_accessor: ITransactionAccessor,
            wallet_accessor: IWalletAccessor,
    ):
        self.balance_service = balance_service
        self.wallet_service = wallet_service
        self.transaction_accessor = transaction_accessor
        self.wallet_accessor = wallet_accessor

    def deposit_money(self, spec: CreateTransactionSpec,
                      customer_context: CustomerContext) -> CreateDepositResult:
        self.wallet_service.validate_if_wallet_is_disabled(wallet_id=customer_context.wallet_id)
        result = self.__create_transaction(
            spec=spec,
            wallet_id=customer_context.wallet_id,
            transaction_type=TransactionType.DEPOSIT
        )
        return CreateDepositResult(
            data=CreateDepositResultData(
                deposit=CreateDepositResultDataDeposit(
                    id=result.id,
                    deposited_by=customer_context.customer_xid,
                    deposited_at=result.transaction_time,
                    amount=result.amount,
                    reference_id=result.reference_id,
                    status=result.status
                )
            ),
            status=ResponseStatus.SUCCESS
        )

    def withdraw_money(self, spec: CreateTransactionSpec,
                       customer_context: CustomerContext) -> CreateWithdrawResult:
        self.wallet_service.validate_if_wallet_is_disabled(wallet_id=customer_context.wallet_id)
        result = self.__create_transaction(
            spec=spec,
            wallet_id=customer_context.wallet_id,
            transaction_type=TransactionType.WITHDRAW
        )
        return CreateWithdrawResult(
            data=CreateWithdrawResultData(
                withdrawal=CreateWithdrawResultDataWithdrawal(
                    id=result.id,
                    withdrawn_by=customer_context.customer_xid,
                    withdrawn_at=result.transaction_time,
                    amount=result.amount,
                    reference_id=result.reference_id,
                    status=result.status
                )
            ),
            status=ResponseStatus.SUCCESS
        )

    def __create_transaction(
            self,
            spec: CreateTransactionSpec,
            wallet_id: str,
            transaction_type: TransactionType
    ) -> CreateTransactionAccessorResult:
        transaction_status = TransactionStatus.SUCCESS if transaction_type == TransactionType.DEPOSIT \
            else self.__validate_transaction(wallet_id=wallet_id, transaction_amount=spec.amount)

        return self.transaction_accessor.create_transaction(
            accessor_spec=CreateTransactionAccessorSpec(
                wallet_id=wallet_id,
                amount=spec.amount,
                reference_id=spec.reference_id,
                type=transaction_type,
                status=transaction_status
            )
        )

    def __validate_transaction(self, wallet_id: str, transaction_amount: Decimal) -> TransactionStatus:
        current_balance = self.balance_service.get_balance_by_wallet_id(
            spec=GetBalanceByWalletIdSpec(
                wallet_id=wallet_id
            )
        ).balance_amount
        return TransactionStatus.SUCCESS if transaction_amount <= current_balance else TransactionStatus.FAIL
