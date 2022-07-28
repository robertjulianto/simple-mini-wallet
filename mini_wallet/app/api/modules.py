from typing import no_type_check

from injector import Module, Binder, singleton

from mini_wallet.core.auth.adapter.authentication_service import AuthenticationService
from mini_wallet.core.auth.port.authentication_service import IAuthenticationService
from mini_wallet.core.balance.adapter.balance_service import BalanceService
from mini_wallet.core.balance.port.balance_service import IBalanceService
from mini_wallet.core.transaction.adapter.transaction_service import TransactionService
from mini_wallet.core.transaction.port.transaction_service import ITransactionService
from mini_wallet.core.wallet.adapter.wallet_service import WalletService
from mini_wallet.core.wallet.port.wallet_service import IWalletService
from mini_wallet.app.api.common.adapters import SessionManager
from mini_wallet.infrastructure.sqlalchemy.ports import ISessionManager


class MiniWalletModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(IWalletService, to=WalletService, scope=singleton)
        binder.bind(IAuthenticationService, to=AuthenticationService, scope=singleton)
        binder.bind(IBalanceService, to=BalanceService, scope=singleton)
        binder.bind(ITransactionService, to=TransactionService, scope=singleton)
        binder.bind(ISessionManager, to=SessionManager, scope=singleton)
