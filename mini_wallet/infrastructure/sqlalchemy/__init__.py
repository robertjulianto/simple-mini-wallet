import uuid

from sqlalchemy import MetaData, Table, Column, String, DateTime, FetchedValue, Numeric, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper

from mini_wallet.core.common.enums import WalletStatus, TransactionStatus, TransactionType
from mini_wallet.core.common.models import Wallet, Transaction

metadata = MetaData(schema='mini_wallet')

mapper(
    Wallet,
    Table(
        'wallet', metadata,
        Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        Column('owner_id', String, nullable=False),
        Column('token', String, nullable=False),
        Column('status', Enum(WalletStatus), nullable=False),
        Column('enabled_at', DateTime, FetchedValue()),
        Column('disabled_at', DateTime, FetchedValue()),
        Column('created_at', DateTime, FetchedValue()),
        Column('created_by', String, FetchedValue()),
        Column('updated_at', DateTime, FetchedValue()),
        Column('updated_by', String, FetchedValue())
    )
)

mapper(
    Transaction,
    Table(
        'transaction', metadata,
        Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        Column('wallet_id', String, ForeignKey('wallet.id')),
        Column('type', Enum(TransactionType), nullable=False),
        Column('status', Enum(TransactionStatus), nullable=False),
        Column('amount', Numeric, nullable=False),
        Column('reference_id', String, nullable=False),
        Column('transaction_time', DateTime, nullable=False),
        Column('created_at', DateTime, FetchedValue()),
        Column('created_by', String, FetchedValue()),
        Column('updated_at', DateTime, FetchedValue()),
        Column('updated_by', String, FetchedValue())
    )
)
