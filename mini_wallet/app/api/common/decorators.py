import inspect
from functools import wraps

from flask import request
from jwt import InvalidTokenError

from mini_wallet.app.api.common.exceptions import FailResponse
from mini_wallet.app.api.di import injector
from mini_wallet.core.auth.port.authentication_service import IAuthenticationService
from mini_wallet.core.common.port.logger import ILogger

logger: ILogger = injector.get(ILogger)  # type: ignore


def authorize():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            authentication_service: IAuthenticationService = injector.get(IAuthenticationService)
            try:
                auth: str = request.headers.get('Authorization')
                if auth and auth.startswith('Token '):
                    token = auth.split(' ', maxsplit=1)[1]
                    customer_context = authentication_service.verify_token(token=token)
                else:
                    raise FailResponse('Invalid token.', 401, error_code='INVALID_TOKEN')
                if inspect.signature(f).parameters.get('customer_context'):
                    return f(*args, **kwargs, customer_context=customer_context)
                return f(*args, **kwargs)
            except InvalidTokenError:
                raise FailResponse('Invalid token.', 401, error_code='INVALID_TOKEN')

        return decorated_function

    return decorator
