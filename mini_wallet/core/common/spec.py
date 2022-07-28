from dataclasses import dataclass
from typing import TypeVar, Generic

from mini_wallet.core.common.enums import ResponseStatus

T = TypeVar('T')


@dataclass
class BaseServiceResult(Generic[T]):
    data: T
    status: ResponseStatus
