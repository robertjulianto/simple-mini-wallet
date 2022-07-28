from typing import no_type_check

from injector import Module, Binder, singleton

from mini_wallet.core.common.port.logger import ILogger
from mini_wallet.infrastructure.common.adapter.logger import Logger


class LoggerInfrastructureModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(ILogger, to=Logger, scope=singleton)
