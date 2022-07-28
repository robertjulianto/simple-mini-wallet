import secrets

from injector import inject

from mini_wallet.core.auth.port.token_provider import ITokenProvider
from mini_wallet.core.common.port.logger import ILogger
from mini_wallet.core.auth.exceptions import ExpiredToken, InvalidToken
from mini_wallet.core.wallet.port.wallet_accessor import IWalletAccessor, GetWalletByTokenAccessorSpec


class JWTProvider(ITokenProvider):
    ALGORITHM = "HS256"
    SECRET_KEY = "MY_SECRET_KEY"

    @inject
    def __init__(
            self,
            logger: ILogger,
            wallet_accessor: IWalletAccessor
    ) -> None:
        self.logger = logger
        self.wallet_accessor = wallet_accessor

    def generate_token(self) -> str:
        token = secrets.token_hex(20)
        return token

    def verify_token(self, token: str) -> dict:
        try:
            get_wallet_by_token_result = self.wallet_accessor.get_wallet_by_token(
                accessor_spec=GetWalletByTokenAccessorSpec(
                    token=token
                )
            )
            return {
                "customer_xid": get_wallet_by_token_result.owner_id,
                "wallet_id": get_wallet_by_token_result.id
            }
        except Exception as e:
            self.logger.error(
                f"Verify token with spec: token = {token} failed because:", e
            )
            raise InvalidToken
