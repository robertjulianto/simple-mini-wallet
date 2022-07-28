from injector import inject

from mini_wallet.core.auth.port.authentication_service import IAuthenticationService, GenerateTokenResult, \
    AuthenticateSpec, CustomerContext
from mini_wallet.core.auth.port.token_provider import ITokenProvider


class AuthenticationService(IAuthenticationService):

    @inject
    def __init__(
            self,
            token_provider: ITokenProvider
    ):
        self.token_provider = token_provider

    def generate_token(self) -> GenerateTokenResult:
        return GenerateTokenResult(
            token=self.token_provider.generate_token()
        )

    def verify_token(self, token: str) -> CustomerContext:
        payload_dict = self.token_provider.verify_token(token)
        return CustomerContext(**payload_dict)

