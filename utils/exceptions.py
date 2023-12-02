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


class AuthenticationError(InvalidCredentialsError):
    """
    Exception to be raised when no/invalid credentials (login or password)
    are provided.
    """
    def __init__(self, msg="Authentication required.", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class AuthorizationError(InvalidCredentialsError):
    """
    Exception to be raised when the user has insufficient authorization
    to perform an action (for instance, action requires admin credentials).
    """
    pass
