from typing import Tuple

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from mini_wallet.app.api.common.decorators import authorize
from mini_wallet.app.api.common.exceptions import FailResponse
from mini_wallet.app.api.common.models import MiniWalletSchema, BaseResponse
from mini_wallet.app.api.di import injector
from mini_wallet.core.auth.port.authentication_service import CustomerContext
from mini_wallet.core.common.enums import TransactionStatus, WalletStatus
from mini_wallet.core.common.exceptions import MiniWalletGeneralException, WalletIsEnabledException, \
    WalletIsDisabledException, TransactionReferenceIsExistsException, EntityAlreadyExistsException
from mini_wallet.core.transaction.port.transaction_service import CreateTransactionSpec, CreateDepositResult, \
    CreateWithdrawResult, ITransactionService
from mini_wallet.core.wallet.port.wallet_service import EnableWalletSpec, EnableWalletResult, IWalletService, \
    ViewWalletSpec, ViewWalletResult, DisableWalletSpec, DisableWalletResult

blp = Blueprint('wallet', __name__)

wallet_service = injector.get(IWalletService)  # type: ignore
transaction_service = injector.get(ITransactionService)  # type: ignore


class WalletResponseDataWallet(MiniWalletSchema):
    id = fields.Str()
    owned_by = fields.Str()
    status = EnumField(WalletStatus, by_value=True)
    enabled_at = fields.DateTime()
    balance = fields.Decimal()


class WalletResponseData(MiniWalletSchema):
    wallet = fields.Nested(WalletResponseDataWallet())


class WalletResponse(BaseResponse):
    data = fields.Nested(WalletResponseData())


@blp.post('/')
@authorize()
@marshal_with(WalletResponse, 201)
def enable_wallet(customer_context: CustomerContext) -> Tuple[EnableWalletResult, int]:
    try:
        spec = EnableWalletSpec(wallet_id=customer_context.wallet_id)
        return wallet_service.enable_wallet(spec=spec), 201
    except WalletIsEnabledException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except MiniWalletGeneralException as e:
        raise FailResponse(str(e), status_code=422)


@blp.get('/')
@authorize()
@marshal_with(WalletResponse, 200)
def view_wallet(customer_context: CustomerContext) -> Tuple[ViewWalletResult, int]:
    try:
        spec = ViewWalletSpec(wallet_id=customer_context.wallet_id)
        return wallet_service.view_wallet(spec=spec), 200
    except WalletIsDisabledException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except MiniWalletGeneralException as e:
        raise FailResponse(str(e), status_code=422)


class DisableWalletResponseDataWallet(MiniWalletSchema):
    id = fields.Str()
    owned_by = fields.Str()
    status = EnumField(WalletStatus, by_value=True)
    disabled_at = fields.DateTime()
    balance = fields.Decimal()


class DisableWalletResponseData(MiniWalletSchema):
    wallet = fields.Nested(DisableWalletResponseDataWallet())


class DisableWalletResponse(BaseResponse):
    data = fields.Nested(DisableWalletResponseData())


@blp.patch('/')
@authorize()
@marshal_with(DisableWalletResponse, 200)
def disable_wallet(customer_context: CustomerContext) -> Tuple[DisableWalletResult, int]:
    try:
        spec = DisableWalletSpec(wallet_id=customer_context.wallet_id)
        return wallet_service.disable_wallet(spec=spec), 200
    except WalletIsDisabledException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except MiniWalletGeneralException as e:
        raise FailResponse(str(e), status_code=422)


class CreateTransactionRequest(MiniWalletSchema):
    amount = fields.Decimal(required=True)
    reference_id = fields.Str(required=True)

    @post_load
    def construct_spec(self, data, **kwargs) -> CreateTransactionSpec:
        return CreateTransactionSpec(**data)


class DepositTransactionResponseDataDeposit(MiniWalletSchema):
    id = fields.Str()
    deposited_by = fields.Str()
    status = EnumField(TransactionStatus, by_value=True)
    deposited_at = fields.Str()
    amount = fields.Str()
    reference_id = fields.Str()


class DepositTransactionResponseData(MiniWalletSchema):
    deposit = fields.Nested(DepositTransactionResponseDataDeposit())


class DepositTransactionResponse(BaseResponse):
    data = fields.Nested(DepositTransactionResponseData())


@blp.post('/deposits')
@authorize()
@use_kwargs(CreateTransactionRequest, location="form")
@marshal_with(DepositTransactionResponse)
def deposit_money(spec: CreateTransactionSpec, customer_context: CustomerContext) -> Tuple[CreateDepositResult, int]:
    try:
        return transaction_service.deposit_money(spec=spec, customer_context=customer_context), 201
    except WalletIsDisabledException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except EntityAlreadyExistsException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except MiniWalletGeneralException as e:
        raise FailResponse(str(e), status_code=422)


class WithdrawTransactionResponseDataWithdraw(MiniWalletSchema):
    id = fields.Str()
    withdrawn_by = fields.Str()
    status = EnumField(TransactionStatus, by_value=True)
    withdrawn_at = fields.Str()
    amount = fields.Str()
    reference_id = fields.Str()


class WithdrawTransactionResponseData(MiniWalletSchema):
    withdrawal = fields.Nested(WithdrawTransactionResponseDataWithdraw())


class WithdrawTransactionResponse(BaseResponse):
    data = fields.Nested(WithdrawTransactionResponseData())


@blp.post('/withdrawals')
@authorize()
@use_kwargs(CreateTransactionRequest, location="form")
@marshal_with(WithdrawTransactionResponse)
def withdraw_money(spec: CreateTransactionSpec, customer_context: CustomerContext) -> Tuple[CreateWithdrawResult, int]:
    try:
        return transaction_service.withdraw_money(spec=spec, customer_context=customer_context), 201
    except WalletIsDisabledException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except EntityAlreadyExistsException as e:
        raise FailResponse(str(e), status_code=422, error_code=e.error_code)
    except MiniWalletGeneralException as e:
        raise FailResponse(str(e), status_code=422)
