from typing import no_type_check

from injector import Module, Binder, singleton

from mini_wallet.core.wallet.port.wallet_accessor import IWalletAccessor
from mini_wallet.infrastructure.wallet.adapter.wallet_accessor import WalletAccessor


class WalletInfrastructureModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(IWalletAccessor, to=WalletAccessor, scope=singleton)
