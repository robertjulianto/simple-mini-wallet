from mini_wallet.core.common.enums import ResponseStatus


class FailResponse(Exception):
    status_code: int = 400
    error_code: str = 'FAIL_RESPONSE'

    def __init__(self, message, status_code=None, error_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code

    def to_dict(self):
        return {
            'data': {
                'exception': {
                    'errorCode': self.error_code,
                    'message': self.message
                }
            },
            'status': ResponseStatus.FAIL.value
        }

    def __str__(self):
        return self.message
