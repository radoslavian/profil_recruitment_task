from hashlib import sha256

from utils.exceptions import AuthenticationError, AuthorizationError

ADMIN_ROLE_NAME = "admin"


def generate_password_hash(password):
    return sha256(bytes(password, "utf-8")).hexdigest()


def check_password_hash(password_hash, password):
    return generate_password_hash(password) == password_hash


def login_required(func):
    def _decorator(self, *args, **kwargs):
        if self._authenticated_user is not None:
            return func(self, *args, **kwargs)
        raise AuthenticationError

    return _decorator


def admin_required(func):
    def _decorator(self, *args, **kwargs):
        if self._authenticated_user.role.name == ADMIN_ROLE_NAME:
            return func(self, *args, **kwargs)
        raise AuthorizationError

    return _decorator
