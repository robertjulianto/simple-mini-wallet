from typing import no_type_check

from injector import Binder, Module, singleton

from mini_wallet.core.auth.port.token_provider import ITokenProvider
from mini_wallet.infrastructure.auth.adapter.token_provider import JWTProvider


class AuthenticationInfrastructureModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(ITokenProvider, to=JWTProvider, scope=singleton)
