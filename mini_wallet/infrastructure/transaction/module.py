from typing import no_type_check

from injector import Module, Binder, singleton

from mini_wallet.core.transaction.port.transaction_accessor import ITransactionAccessor
from mini_wallet.infrastructure.transaction.adapter.transaction_accessor import TransactionAccessor


class TransactionInfrastructureModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(ITransactionAccessor, to=TransactionAccessor, scope=singleton)
