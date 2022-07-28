from datetime import datetime, timezone
from decimal import Decimal

from injector import inject

from mini_wallet.core.auth.port.authentication_service import IAuthenticationService, AuthenticateSpec
from mini_wallet.core.balance.port.balance_service import IBalanceService, GetBalanceByWalletIdSpec
from mini_wallet.core.common.enums import ResponseStatus, WalletStatus
from mini_wallet.core.common.exceptions import MiniWalletGeneralException, WalletIsEnabledException, \
    WalletIsDisabledException
from mini_wallet.core.common.port.logger import ILogger
from mini_wallet.core.wallet.port.wallet_accessor import IWalletAccessor, CreateWalletAccessorSpec, \
    GetWalletByIdAccessorSpec, UpdateWalletStatusAccessorSpec
from mini_wallet.core.wallet.port.wallet_service import IWalletService, CreateWalletSpec, CreateWalletResult, \
    CreateWalletResultData, EnableWalletSpec, EnableWalletResult, ViewWalletSpec, \
    ViewWalletResult, DisableWalletResult, DisableWalletSpec, WalletData, EnabledWalletResultData, EnabledWalletData, \
    DisabledWalletData, DisabledWalletResultData


class WalletService(IWalletService):

    @inject
    def __init__(
            self,
            wallet_accessor: IWalletAccessor,
            authentication_service: IAuthenticationService,
            balance_service: IBalanceService,
            logger: ILogger
    ):
        self.wallet_accessor = wallet_accessor
        self.authentication_service = authentication_service
        self.logger = logger
        self.balance_service = balance_service

    def create_wallet(self, spec: CreateWalletSpec) -> CreateWalletResult:
        try:
            token = self.authentication_service.generate_token().token
            self.wallet_accessor.create_wallet(
                accessor_spec=CreateWalletAccessorSpec(
                    owner_id=spec.customer_xid,
                    token=token
                )
            )

            return CreateWalletResult(
                data=CreateWalletResultData(
                    token=token
                ),
                status=ResponseStatus.SUCCESS
            )
        except Exception as e:
            self.logger.error(str(e))
            raise e

    def enable_wallet(self, spec: EnableWalletSpec) -> EnableWalletResult:
        self.validate_if_wallet_is_enabled(wallet_id=spec.wallet_id)
        result = self.wallet_accessor.update_wallet_status(
            accessor_spec=UpdateWalletStatusAccessorSpec(
                id=spec.wallet_id,
                enabled_at=datetime.now(tz=timezone.utc),
                status=WalletStatus.ENABLED
            )
        )
        current_balance = self.__get_current_balance_by_wallet_id(wallet_id=result.id)
        return EnableWalletResult(
            data=EnabledWalletResultData(
                wallet=EnabledWalletData(
                    id=result.id,
                    owned_by=result.owner_id,
                    status=result.status,
                    enabled_at=result.enabled_at,
                    balance=current_balance
                )
            ),
            status=ResponseStatus.SUCCESS
        )

    def view_wallet(self, spec: ViewWalletSpec) -> ViewWalletResult:
        self.validate_if_wallet_is_disabled(wallet_id=spec.wallet_id)
        result = self.wallet_accessor.get_wallet_by_id(
            accessor_spec=GetWalletByIdAccessorSpec(
                id=spec.wallet_id
            )
        )
        current_balance = self.__get_current_balance_by_wallet_id(wallet_id=result.id)
        return ViewWalletResult(
            data=EnabledWalletResultData(
                wallet=EnabledWalletData(
                    id=result.id,
                    owned_by=result.owner_id,
                    status=result.status,
                    enabled_at=result.enabled_at,
                    balance=current_balance
                )
            ),
            status=ResponseStatus.SUCCESS
        )

    def disable_wallet(self, spec: DisableWalletSpec) -> DisableWalletResult:
        self.validate_if_wallet_is_disabled(wallet_id=spec.wallet_id)
        result = self.wallet_accessor.update_wallet_status(
            accessor_spec=UpdateWalletStatusAccessorSpec(
                id=spec.wallet_id,
                disabled_at=datetime.now(tz=timezone.utc),
                status=WalletStatus.DISABLED
            )
        )
        current_balance = self.__get_current_balance_by_wallet_id(wallet_id=result.id)
        return DisableWalletResult(
            data=DisabledWalletResultData(
                wallet=DisabledWalletData(
                    id=result.id,
                    owned_by=result.owner_id,
                    status=result.status,
                    disabled_at=result.disabled_at,
                    balance=current_balance
                )
            ),
            status=ResponseStatus.SUCCESS
        )

    def __get_current_balance_by_wallet_id(self, wallet_id: str) -> Decimal:
        result = self.balance_service.get_balance_by_wallet_id(
            spec=GetBalanceByWalletIdSpec(
                wallet_id=wallet_id
            )
        )
        return result.balance_amount

    def validate_if_wallet_is_enabled(self, wallet_id: str):
        wallet = self.wallet_accessor.get_wallet_by_id(
            accessor_spec=GetWalletByIdAccessorSpec(id=wallet_id)
        )
        if wallet.status == WalletStatus.ENABLED:
            raise WalletIsEnabledException()

    def validate_if_wallet_is_disabled(self, wallet_id: str):
        wallet = self.wallet_accessor.get_wallet_by_id(
            accessor_spec=GetWalletByIdAccessorSpec(id=wallet_id)
        )
        if wallet.status == WalletStatus.DISABLED:
            raise WalletIsDisabledException()
