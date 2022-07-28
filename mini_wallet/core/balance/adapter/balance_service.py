from decimal import Decimal

from injector import inject

from mini_wallet.core.balance.port.balance_service import IBalanceService, GetBalanceByWalletIdSpec, \
    GetBalanceByWalletIdResult
from mini_wallet.core.common.enums import TransactionStatus, TransactionType
from mini_wallet.core.transaction.port.transaction_accessor import ITransactionAccessor, GetTransactionByWalletIdSpec


class BalanceService(IBalanceService):

    @inject
    def __init__(
            self,
            transaction_accessor: ITransactionAccessor
    ):
        self.transaction_accessor = transaction_accessor

    def get_balance_by_wallet_id(self, spec: GetBalanceByWalletIdSpec) -> GetBalanceByWalletIdResult:
        current_balance = Decimal(0)
        result = self.transaction_accessor.get_transactions_by_wallet_id(
            accessor_spec=GetTransactionByWalletIdSpec(
                wallet_id=spec.wallet_id
            )
        )
        if result.transactions:
            for transaction in result.transactions:
                if transaction.status == TransactionStatus.SUCCESS:
                    amount = transaction.amount * (1 if transaction.type == TransactionType.DEPOSIT else -1)
                    current_balance = current_balance + amount

        return GetBalanceByWalletIdResult(
            balance_amount=current_balance
        )
