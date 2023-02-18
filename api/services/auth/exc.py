class AuthenticationException(Exception):
    """Base exception for all authentication exceptions"""


class UnauthenticatedError(AuthenticationException):
    """An error that is raised when authentication is not present"""


class UnauthorizedError(Exception):
    """An error that is raised when authorization is not passed"""


class BadCredentialsError(AuthenticationException):
    """An error that is raised when bad credentials are passed"""


class UserNotFoundError(Exception):
    pass
