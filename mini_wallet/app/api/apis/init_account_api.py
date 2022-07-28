from typing import Tuple

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from marshmallow import fields, post_load

from mini_wallet.app.api.common.models import MiniWalletSchema, BaseResponse
from mini_wallet.app.api.di import injector
from mini_wallet.core.wallet.port.wallet_service import IWalletService, CreateWalletResult, CreateWalletSpec

blp = Blueprint('init', __name__)

wallet_service = injector.get(IWalletService)  # type: ignore


class InitAccountWalletRequest(MiniWalletSchema):
    customer_xid = fields.Str(required=True)

    @post_load
    def __construct_spec(self, data, **kwargs) -> CreateWalletSpec:
        return CreateWalletSpec(**data)


class InitAccountWalletResponseData(MiniWalletSchema):
    token = fields.Str()


class InitAccountWalletResponse(BaseResponse):
    data = fields.Nested(InitAccountWalletResponseData())


@blp.post('/')
@use_kwargs(InitAccountWalletRequest, location="form")
@marshal_with(InitAccountWalletResponse)
def get_transactions_paginated(spec: CreateWalletSpec) -> Tuple[CreateWalletResult, int]:
    return wallet_service.create_wallet(spec=spec), 201
