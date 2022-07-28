from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest
from pytest_bdd import scenario, given, parsers, when, then
from sqlalchemy import select

from mini_wallet.core.common.enums import TransactionType, TransactionStatus, ResponseStatus
from mini_wallet.core.common.exceptions import WalletIsEnabledException, WalletIsDisabledException
from mini_wallet.core.common.models import Transaction, Wallet
from mini_wallet.core.transaction.port.transaction_service import CreateTransactionSpec
from tests.utils import get_transaction_data, assert_equal_exception


@scenario('transaction.feature', 'Deposit money')
def test_deposit_money():
    pass


@scenario('transaction.feature', 'Withdraw money')
def test_withdraw_money():
    pass


@scenario('transaction.feature', 'Deposit money into disabled wallet')
def test_deposit_money_into_disabled_wallet():
    pass


@scenario('transaction.feature', 'Withdraw money into disabled wallet')
def test_withdraw_money_into_disabled_wallet():
    pass


@given(
    parsers.parse("{} amount is {transaction_amount}"),
    converters={"transaction_amount": str},
    target_fixture="transaction_amount_spec"
)
def transaction_amount_value_spec(transaction_amount):
    return Decimal(transaction_amount.replace(".", ""))


@given(
    parsers.parse("Reference id is {reference_id}"),
    converters={"reference_id": str},
    target_fixture="reference_id_spec"
)
def reference_id_value_spec(reference_id):
    return reference_id


@given(
    parsers.parse("{} time is now"),
    target_fixture="transaction_time_spec"
)
def deposit_time_is_now():
    return datetime.now(tz=timezone.utc)


@when(parsers.parse("I deposit money"), target_fixture="create_transaction_result")
def i_deposit_money(mock_transaction_service, customer_context_spec, transaction_amount_spec, reference_id_spec):
    spec = CreateTransactionSpec(
        amount=transaction_amount_spec,
        reference_id=reference_id_spec
    )
    return mock_transaction_service().deposit_money(spec=spec, customer_context=customer_context_spec)


@when(parsers.parse("I deposit money into disabled wallet"),
      target_fixture="create_transaction_into_disabled_money_result")
def i_deposit_money_into_disabled_wallet(mock_transaction_service, customer_context_spec, transaction_amount_spec,
                                         reference_id_spec):
    spec = CreateTransactionSpec(
        amount=transaction_amount_spec,
        reference_id=reference_id_spec
    )
    return pytest.raises(
        WalletIsDisabledException,
        mock_transaction_service().deposit_money,
        spec=spec, customer_context=customer_context_spec
    )


@when(parsers.parse("I withdraw money"), target_fixture="create_transaction_result")
def i_withdraw_money(mock_transaction_service, customer_context_spec, transaction_amount_spec, reference_id_spec):
    spec = CreateTransactionSpec(
        amount=transaction_amount_spec,
        reference_id=reference_id_spec
    )
    return mock_transaction_service().withdraw_money(spec=spec, customer_context=customer_context_spec)


@when(parsers.parse("I withdraw money into disabled wallet"),
      target_fixture="create_transaction_into_disabled_money_result")
def i_withdraw_money_into_disabled_wallet(mock_transaction_service, customer_context_spec, transaction_amount_spec,
                                          reference_id_spec):
    spec = CreateTransactionSpec(
        amount=transaction_amount_spec,
        reference_id=reference_id_spec
    )
    return pytest.raises(
        WalletIsDisabledException,
        mock_transaction_service().deposit_money,
        spec=spec, customer_context=customer_context_spec
    )


@then("Transaction is created", target_fixture="transaction_is_created_result")
def transaction_is_created(create_transaction_result, session_manager):
    transaction_data = get_transaction_data(create_transaction_result)
    get_transaction_query = select(Transaction).where(Transaction.id == transaction_data.id)
    with session_manager.get_session_scope() as sess:
        transaction = sess.execute(get_transaction_query).scalar()
    assert transaction
    return transaction


@then(parsers.parse("Transaction type is {transaction_type}"), converters={"transaction_type": str})
def assert_transaction_type(transaction_is_created_result, transaction_type):
    assert transaction_is_created_result.type == TransactionType[transaction_type.upper()]


@then(parsers.parse("Transaction status is {transaction_status}"), converters={"transaction_status": str})
def assert_transaction_status(transaction_is_created_result, create_transaction_result, transaction_status):
    transaction_data = get_transaction_data(create_transaction_result)
    assert transaction_is_created_result.status == TransactionStatus[transaction_status.upper()]
    assert transaction_data.status == TransactionStatus[transaction_status.upper()]


@then("Deposit by me")
def assert_deposit_by(create_transaction_result, customer_context_spec):
    transaction_data = get_transaction_data(create_transaction_result)
    assert transaction_data.deposited_by == customer_context_spec.customer_xid


@then("Withdraw by me")
def assert_deduct_by(create_transaction_result, customer_context_spec):
    transaction_data = get_transaction_data(create_transaction_result)
    assert transaction_data.withdrawn_by == customer_context_spec.customer_xid


@then(parsers.parse("Amount is {amount}"), converters={"amount": str})
def assert_amount(transaction_is_created_result, create_transaction_result, amount):
    transaction_data = get_transaction_data(create_transaction_result)
    assert transaction_is_created_result.amount == Decimal(amount.replace(".", ""))
    assert transaction_data.amount == Decimal(amount.replace(".", ""))


@then(parsers.parse("Reference id is {reference_id}"), converters={"reference_id": str})
def assert_reference_id(transaction_is_created_result, create_transaction_result, reference_id_spec):
    transaction_data = get_transaction_data(create_transaction_result)
    assert transaction_is_created_result.reference_id == reference_id_spec
    assert transaction_data.reference_id == reference_id_spec


@then(parsers.parse("{} money is success"))
def assert_create_transaction_status(create_transaction_result):
    assert create_transaction_result.status == ResponseStatus.SUCCESS


@then("I get error that wallet is already disabled")
def i_get_error_that_wallet_is_already_disabled(create_transaction_into_disabled_money_result):
    assert_equal_exception(create_transaction_into_disabled_money_result, WalletIsDisabledException())
