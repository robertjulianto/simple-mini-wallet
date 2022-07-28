class InvalidToken(Exception):
    def __str__(self) -> str:
        return "Invalid token."


class ExpiredToken(Exception):
    def __str__(self) -> str:
        return "Token is expired."


class ExpiredTokenException(Exception):
    status_code = 401
    message = 'Session expired'
    error_code = 'TOKEN_EXPIRED'

    def __init__(self):
        Exception.__init__(self)

    def to_dict(self):
        return {'message': self.message, 'errorCode': self.error_code}

    def __str__(self):
        return self.message
