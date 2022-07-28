def get_transaction_data(create_transaction_result):
    transaction_data_dict = create_transaction_result.data.__dict__
    return transaction_data_dict.get('deposit') or transaction_data_dict.get('withdrawal')


def assert_equal_exception(actual, expected):
    assert actual.type == expected.__class__
    assert actual.value.error_code == expected.error_code
    assert actual.value.message == expected.message
