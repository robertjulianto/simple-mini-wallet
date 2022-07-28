from injector import inject
from sqlalchemy import insert, update, select

from mini_wallet.core.common.enums import WalletStatus
from mini_wallet.core.common.models import Wallet
from mini_wallet.core.wallet.port.wallet_accessor import IWalletAccessor, CreateWalletAccessorSpec, \
    CreateWalletAccessorResult, GetWalletByIdAccessorSpec, \
    GetWalletByIdAccessorResult, UpdateWalletStatusAccessorSpec, UpdateWalletStatusAccessorResult, \
    GetWalletByTokenAccessorSpec, GetWalletByTokenAccessorResult
from mini_wallet.infrastructure.sqlalchemy.ports import ISessionManager


class WalletAccessor(IWalletAccessor):

    @inject
    def __init__(
            self,
            session_manager: ISessionManager,
    ):
        self.session_manager = session_manager

    def create_wallet(self, accessor_spec: CreateWalletAccessorSpec) -> CreateWalletAccessorResult:
        insert_wallet_query = insert(Wallet).values(
            **accessor_spec.__dict__,
            status=WalletStatus.DISABLED,
        ).returning(Wallet.id)
        with self.session_manager.get_session_scope() as sess:
            result = sess.execute(insert_wallet_query).first()
            sess.commit()
        return CreateWalletAccessorResult(**result)

    def update_wallet_status(self, accessor_spec: UpdateWalletStatusAccessorSpec) -> UpdateWalletStatusAccessorResult:
        update_wallet_status = update(Wallet).values(
            **accessor_spec.__dict__
        ).where(
            Wallet.id == accessor_spec.id
        ).returning(
            Wallet.id,
            Wallet.owner_id,
            Wallet.status,
            Wallet.enabled_at,
            Wallet.disabled_at
        )
        with self.session_manager.get_session_scope() as sess:
            result = sess.execute(update_wallet_status).first()
            sess.commit()
        return UpdateWalletStatusAccessorResult(**result)

    def get_wallet_by_id(self, accessor_spec: GetWalletByIdAccessorSpec) -> GetWalletByIdAccessorResult:
        get_query = select(
            Wallet.id,
            Wallet.owner_id,
            Wallet.status,
            Wallet.enabled_at
        ).where(Wallet.id == accessor_spec.id)
        with self.session_manager.get_session_scope() as sess:
            result = sess.execute(get_query).first()
        return GetWalletByIdAccessorResult(**result)

    def get_wallet_by_token(self, accessor_spec: GetWalletByTokenAccessorSpec) -> GetWalletByTokenAccessorResult:
        get_query = select(
            Wallet.id,
            Wallet.owner_id,
            Wallet.status,
            Wallet.enabled_at
        ).where(Wallet.token == accessor_spec.token)
        with self.session_manager.get_session_scope() as sess:
            result = sess.execute(get_query).first()
        return GetWalletByTokenAccessorResult(**result)
