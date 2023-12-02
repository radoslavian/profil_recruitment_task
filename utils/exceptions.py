class InvalidInputError(ValueError):
    pass


class InvalidEmailError(InvalidInputError):
    pass


class InvalidPhoneNumberError(InvalidInputError):
    pass


class RoleNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    """
    Base class for authorization/authentication errors.
    """
    pass


class InvalidAuthenticationError(InvalidCredentialsError):
    """
    Exception to be raised when no/invalid credentials (login or password)
    are provided.
    """
    pass


class InvalidAuthorizationError(InvalidCredentialsError):
    """
    Exception to be raised when the user has insufficient authorization
    to perform an action (for instance, action requires admin credentials).
    """
    pass
