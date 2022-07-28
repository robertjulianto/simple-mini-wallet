from typing import Any


class MiniWalletGeneralException(Exception):
    message = "Unexpected error occurred."
    error_code = "MINI_WALLET_GENERAL_EXCEPTION"

    def __str__(self):
        return self.message


class WalletIsEnabledException(MiniWalletGeneralException):
    message = "Wallet is already enabled."
    error_code = "WALLET_ENABLED_EXCEPTION"


class WalletIsDisabledException(MiniWalletGeneralException):
    message = "Wallet is already disabled."
    error_code = "WALLET_DISABLED_EXCEPTION"


class TransactionReferenceIsExistsException(MiniWalletGeneralException):
    message = "Transaction reference id is already exists"
    error_code = "TRANSACTION_REF_ID_EXISTS_EXCEPTION"


class EntityAlreadyExistsException(MiniWalletGeneralException):
    error_code = 'ENTITY_ALREADY_EXISTS'

    def __init__(self, entity: str, entity_id: Any, entity_id_name: str = 'id'):
        self.message = f'{entity.capitalize()} with {entity_id_name} {entity_id} is already exists.'

    def __str__(self):
        return self.message


class EntityNotFoundException(MiniWalletGeneralException):
    error_code = 'ENTITY_NOT_FOUND'

    def __init__(self, entity: str, entity_id: Any, entity_id_name: str = 'id'):
        self.message = f'{entity.capitalize()} with {entity_id_name} {entity_id} is not found.'

    def __str__(self):
        return self.message
