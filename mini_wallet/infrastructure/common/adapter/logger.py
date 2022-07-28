import logging
from typing import Optional

from mini_wallet.core.common.port.logger import ILogger


class Logger(ILogger):
    logging.getLogger().setLevel(logging.DEBUG)

    def info(self, msg: str) -> None:
        logging.info(msg)

    def warn(self, msg: str) -> None:
        logging.warning(msg)

    """
    extra parameter is used to add additional data to our sentry event. it will not be logged in the cloudwatch log. 
    use extra field only for additional data. essential data like data model id should be in the msg parameter.
    ps: maximum number of keys for extra data stored in sentry event is 10
    """

    def error(self, msg: str, exception: Optional[Exception] = None, extra: dict = None) -> None:
        if exception is not None:
            logging.exception(msg, extra=extra)
        else:
            logging.error(msg, extra=extra)
