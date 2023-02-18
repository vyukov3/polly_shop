class JwtException(Exception):
    def __init__(self, *args, msg: str | None = None, **kwargs):
        if msg is None:
            msg = self.__class__.__doc__
        super().__init__(msg, *args, **kwargs)


class TokenDecodeError(JwtException):
    """Token decode error"""


class InvalidTokenTypeError(JwtException):
    def __init__(self, token_type: str, expected_type: str):
        super().__init__(f"Got {token_type} token when {expected_type} token was expected")


class TokenNotFoundError(JwtException):
    pass


class InvalidAuthorizationHeaderError(JwtException):
    """Invalid Authorization header"""


class UserRefreshTokenNotFoundError(JwtException):
    pass


class WrongRefreshTokenError(JwtException):
    """Provided refresh token is out of date"""


class AccessTokenRequired(JwtException):
    """Access token is required"""


class RefreshTokenRequired(JwtException):
    """Refresh token is required"""


class TokenRevokedError(JwtException):
    """Provided token has been revoked"""
