from injector import inject
from sqlalchemy import insert, select

from mini_wallet.core.common.models import Transaction
from mini_wallet.core.transaction.port.transaction_accessor import ITransactionAccessor, CreateTransactionAccessorSpec, \
    CreateTransactionAccessorResult, GetTransactionByWalletIdSpec, GetTransactionsByWalletIdResult, \
    BaseTransactionAccessorResult, GetTransactionByReferenceIdSpec, GetTransactionByReferenceIdResult
from mini_wallet.infrastructure.sqlalchemy.ports import ISessionManager


class TransactionAccessor(ITransactionAccessor):

    @inject
    def __init__(
            self,
            session_manager: ISessionManager
    ):
        self.session_manager = session_manager

    def create_transaction(
            self,
            accessor_spec: CreateTransactionAccessorSpec
    ) -> CreateTransactionAccessorResult:
        insert_transaction_query = insert(Transaction).values(
            **accessor_spec.__dict__
        ).returning(
            Transaction.id,
            Transaction.wallet_id,
            Transaction.status,
            Transaction.transaction_time,
            Transaction.amount,
            Transaction.reference_id,
            Transaction.type
        )
        with self.session_manager.get_session_scope() as sess:
            result = sess.execute(insert_transaction_query).first()
            sess.commit()
        return CreateTransactionAccessorResult(**result)

    def get_transactions_by_wallet_id(
            self,
            accessor_spec: GetTransactionByWalletIdSpec
    ) -> GetTransactionsByWalletIdResult:
        get_query = select(
            Transaction.id,
            Transaction.wallet_id,
            Transaction.status,
            Transaction.transaction_time,
            Transaction.amount,
            Transaction.reference_id,
            Transaction.type
        ).where(Transaction.wallet_id == accessor_spec.wallet_id)
        with self.session_manager.get_session_scope() as sess:
            results = sess.execute(get_query).all()
            return GetTransactionsByWalletIdResult(
                transactions=[BaseTransactionAccessorResult(**result) for result in results]
            )

    def get_transactions_by_reference_id(
            self,
            accessor_spec: GetTransactionByReferenceIdSpec
    ) -> GetTransactionByReferenceIdResult:
        get_query = select(
            Transaction.id,
        ).where(Transaction.reference_id == accessor_spec.reference_id)
        with self.session_manager.get_session_scope() as sess:
            result = sess.execute(get_query).first()
            return GetTransactionByReferenceIdResult(
                transaction_id=result.id
            )
