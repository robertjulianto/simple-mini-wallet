from decimal import Decimal

import pytest
from pytest_bdd import scenario, when, then, given, parsers
from sqlalchemy.sql import select

from mini_wallet.core.common.enums import WalletStatus, ResponseStatus
from mini_wallet.core.common.exceptions import WalletIsEnabledException, WalletIsDisabledException
from mini_wallet.core.common.models import Wallet
from mini_wallet.core.wallet.port.wallet_service import EnableWalletSpec, \
    ViewWalletSpec, DisableWalletSpec
from tests.utils import assert_equal_exception


@scenario('wallet.feature', 'Create Wallet')
def test_create_wallet():
    pass


@scenario('wallet.feature', 'Enable Wallet')
def test_enable_wallet():
    pass


@scenario('wallet.feature', 'View Wallet')
def test_view_wallet():
    pass


@scenario('wallet.feature', 'Disable Wallet')
def test_disable_wallet():
    pass


@scenario('wallet.feature', 'Enable Enabled Wallet')
def test_enable_enabled_wallet():
    pass


@scenario('wallet.feature', 'Disable Disabled Wallet')
def test_disable_disabled_wallet():
    pass


@scenario('wallet.feature', 'View Disabled Wallet')
def test_view_disabled_wallet():
    pass


@when('I view wallet', target_fixture='wallet_action_result')
def i_view_wallet(mock_wallet_service, customer_context_spec):
    return mock_wallet_service().view_wallet(spec=ViewWalletSpec(wallet_id=customer_context_spec.wallet_id))


@when('I enable enabled wallet', target_fixture='enable_enabled_wallet_result')
def i_enable_enabled_wallet(mock_wallet_service, customer_context_spec):
    return pytest.raises(
        WalletIsEnabledException,
        mock_wallet_service().enable_wallet,
        spec=DisableWalletSpec(wallet_id=customer_context_spec.wallet_id)
    )


@when('I disable disabled wallet', target_fixture='action_disabled_wallet_result')
def i_disable_disabled_wallet(mock_wallet_service, customer_context_spec):
    return pytest.raises(
        WalletIsDisabledException,
        mock_wallet_service().disable_wallet,
        spec=DisableWalletSpec(wallet_id=customer_context_spec.wallet_id)
    )


@when('I view disabled wallet', target_fixture='action_disabled_wallet_result')
def i_view_disabled_wallet(mock_wallet_service, customer_context_spec):
    return pytest.raises(
        WalletIsDisabledException,
        mock_wallet_service().view_wallet,
        spec=DisableWalletSpec(wallet_id=customer_context_spec.wallet_id)
    )


@then('Wallet is created', target_fixture='wallet_is_created_result')
def wallet_is_created(session_manager, customer_xid_spec):
    get_query = select(Wallet).where(Wallet.owner_id == customer_xid_spec)
    with session_manager.get_session_scope() as session:
        wallet = session.execute(get_query).scalar()
    assert wallet.id
    assert wallet.owner_id == customer_xid_spec
    return wallet


@then('Initial wallet status is disabled')
def initial_wallet_status_is_disabled(wallet_is_created_result):
    assert wallet_is_created_result.status == WalletStatus.DISABLED


@then('I get token')
def i_get_token(create_wallet_result):
    assert create_wallet_result
    assert create_wallet_result.data.token


@then('Creating wallet is success')
def creating_wallet_is_success(create_wallet_result):
    assert create_wallet_result.status == ResponseStatus.SUCCESS


@then('Wallet status is enabled')
def wallet_status_is_enabled(session_manager, wallet_action_result):
    get_query = select(Wallet).where(Wallet.owner_id == wallet_action_result.data.wallet.owned_by)
    with session_manager.get_session_scope() as session:
        wallet = session.execute(get_query).scalar()
    assert wallet.status == WalletStatus.ENABLED


@then("Owner is me")
def own_by_me(wallet_action_result, customer_context_spec):
    assert wallet_action_result.data.wallet.owned_by == customer_context_spec.customer_xid


@then(parsers.parse("Balance is {balance_amount}"), converters={"balance_amount": str})
def assert_current_balance(wallet_action_result, balance_amount):
    assert wallet_action_result.data.wallet.balance == Decimal(balance_amount.replace(".", ""))


@then('Enabling wallet is success')
def enabling_wallet_is_success(wallet_action_result):
    assert wallet_action_result.status == ResponseStatus.SUCCESS


@then('Wallet is returned')
def wallet_is_returned(wallet_action_result):
    assert wallet_action_result


@then('Viewing wallet is success')
def viewing_wallet_is_success(wallet_action_result):
    assert wallet_action_result.status == ResponseStatus.SUCCESS


@then('Wallet status is disabled')
def wallet_status_is_disabled(session_manager, wallet_action_result):
    get_query = select(Wallet).where(Wallet.owner_id == wallet_action_result.data.wallet.owned_by)
    with session_manager.get_session_scope() as session:
        wallet = session.execute(get_query).scalar()
    assert wallet.status == WalletStatus.DISABLED


@then('Disabling wallet is success')
def disabling_wallet_is_success(wallet_action_result):
    assert wallet_action_result.status == ResponseStatus.SUCCESS


@then("I get error that wallet is already enabled")
def i_get_error_that_wallet_is_already_enabled(enable_enabled_wallet_result):
    assert_equal_exception(enable_enabled_wallet_result, WalletIsEnabledException())


@then("I get error that wallet is already disabled")
def i_get_error_that_wallet_is_already_disabled(action_disabled_wallet_result):
    assert_equal_exception(action_disabled_wallet_result, WalletIsDisabledException())
