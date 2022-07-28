import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest
from injector import Injector
from pytest_bdd import given, when, parsers
from sqlalchemy import select

from mini_wallet.core.auth.port.authentication_service import CustomerContext
from mini_wallet.core.common.models import Wallet
from mini_wallet.core.transaction.port.transaction_service import ITransactionService, CreateTransactionSpec
from mini_wallet.core.wallet.port.wallet_service import IWalletService, CreateWalletSpec, EnableWalletSpec, \
    DisableWalletSpec
from mini_wallet.infrastructure.auth.module import AuthenticationInfrastructureModule
from mini_wallet.infrastructure.common.modules import LoggerInfrastructureModule
from mini_wallet.infrastructure.sqlalchemy.ports import ISessionManager
from mini_wallet.infrastructure.transaction.module import TransactionInfrastructureModule
from mini_wallet.infrastructure.wallet.module import WalletInfrastructureModule
from tests.adapter.session_manager import FakeSessionManager
from tests.modules import TestMiniWalletModule


@pytest.fixture
def injector():
    os.environ['APP_ENV'] = 'unittest'
    injector = Injector([
        TestMiniWalletModule,
        LoggerInfrastructureModule,
        WalletInfrastructureModule,
        AuthenticationInfrastructureModule,
        TransactionInfrastructureModule
    ])
    yield injector
    session_manager: FakeSessionManager = injector.get(ISessionManager)  # noqa
    session_manager.tear_down()


@pytest.fixture
def session_manager(injector: Injector):
    return injector.get(ISessionManager)  # type: ignore


@pytest.fixture
def mock_wallet_service(injector):
    def factory():
        return injector.get(IWalletService)

    return factory


@pytest.fixture
def mock_transaction_service(injector):
    def factory():
        return injector.get(ITransactionService)

    return factory


@given('I have customer id', target_fixture='customer_xid_spec')
def i_have_customer_id():
    return '0f6544af-13a4-dc81-c780-08202256cdb9'


@given('I have enabled wallet', target_fixture='customer_context_spec')
def i_have_wallet(mock_wallet_service, session_manager, customer_xid_spec):
    mock_wallet_service().create_wallet(spec=CreateWalletSpec(customer_xid=customer_xid_spec))
    get_wallet_id = select(Wallet.id).where(Wallet.owner_id == customer_xid_spec)
    with session_manager.get_session_scope() as sess:
        wallet_id = sess.execute(get_wallet_id).scalar()
    mock_wallet_service().enable_wallet(spec=EnableWalletSpec(wallet_id=wallet_id))
    return CustomerContext(
        customer_xid=customer_xid_spec,
        wallet_id=wallet_id,
    )


@given('I have disabled wallet', target_fixture='customer_context_spec')
def i_have_disabled_wallet(mock_wallet_service, session_manager, customer_xid_spec):
    mock_wallet_service().create_wallet(spec=CreateWalletSpec(customer_xid=customer_xid_spec))
    get_wallet_id = select(Wallet.id).where(Wallet.owner_id == customer_xid_spec)
    with session_manager.get_session_scope() as sess:
        wallet_id = sess.execute(get_wallet_id).scalar()
    return CustomerContext(
        customer_xid=customer_xid_spec,
        wallet_id=wallet_id,
    )


@when('I create wallet', target_fixture='create_wallet_result')
def i_create_wallet(mock_wallet_service, customer_xid_spec):
    return mock_wallet_service().create_wallet(spec=CreateWalletSpec(customer_xid=customer_xid_spec))


@given(
    parsers.parse("I have balance {balance_amount}"),
    converters={"balance_amount": str}
)
def i_have_balance(mock_transaction_service, customer_context_spec, balance_amount):
    balance = Decimal(balance_amount.replace(".", ""))
    if balance == Decimal(0):
        return
    spec = CreateTransactionSpec(
        amount=balance,
        reference_id="DUMMY_DEPOSIT"
    )
    mock_transaction_service().deposit_money(spec=spec, customer_context=customer_context_spec)


@when('I enable wallet', target_fixture='wallet_action_result')
@given('My walled is enabled')
def i_enable_wallet(mock_wallet_service, customer_context_spec):
    return mock_wallet_service().enable_wallet(spec=EnableWalletSpec(wallet_id=customer_context_spec.wallet_id))


@when('I disable wallet', target_fixture='wallet_action_result')
@given('My wallet is disabled')
def i_disable_wallet(mock_wallet_service, customer_context_spec):
    return mock_wallet_service().disable_wallet(spec=DisableWalletSpec(wallet_id=customer_context_spec.wallet_id))
