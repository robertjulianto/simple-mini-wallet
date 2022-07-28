from injector import Injector

from mini_wallet.app.api.modules import MiniWalletModule
from mini_wallet.infrastructure.auth.module import AuthenticationInfrastructureModule
from mini_wallet.infrastructure.common.modules import LoggerInfrastructureModule
from mini_wallet.infrastructure.transaction.module import TransactionInfrastructureModule
from mini_wallet.infrastructure.wallet.module import WalletInfrastructureModule

injector = Injector([
    MiniWalletModule,
    WalletInfrastructureModule,
    LoggerInfrastructureModule,
    AuthenticationInfrastructureModule,
    TransactionInfrastructureModule
])
