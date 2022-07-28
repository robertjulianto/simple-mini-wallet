from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda e: e, cls))

    @classmethod
    def names(cls):
        return list(map(lambda e: e.name, cls))

    @classmethod
    def values(cls):
        return list(map(lambda e: e.value, cls))

    @classmethod
    def has_name(cls, key):
        return key in cls._member_names_

    def __str__(self) -> str:
        return self.name


class WalletStatus(ExtendedEnum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'


class TransactionStatus(ExtendedEnum):
    SUCCESS = 'success'
    FAIL = 'fail'


class ResponseStatus(ExtendedEnum):
    SUCCESS = 'success'
    FAIL = 'fail'


class TransactionType(ExtendedEnum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
