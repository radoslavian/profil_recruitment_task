class InvalidInputError(ValueError):
    pass


class InvalidEmailError(InvalidInputError):
    pass


class InvalidPhoneNumberError(InvalidInputError):
    pass


class RoleNotFoundError(Exception):
    pass
