from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from mini_wallet.core.common.enums import WalletStatus, TransactionStatus, TransactionType


@dataclass
class Wallet:
    id: UUID
    owner_id: str
    token: str
    status: WalletStatus
    enabled_at: Optional[datetime]
    disabled_at: Optional[datetime]
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime]
    updated_by: Optional[str]


@dataclass
class Transaction:
    id: str
    wallet_id: str
    type: TransactionType
    amount: Decimal
    status: TransactionStatus
    reference_id: str
    transaction_time: datetime
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime]
    updated_by: Optional[str]
