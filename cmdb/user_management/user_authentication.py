import logging

CMDB_LOGGER = logging.getLogger(__name__)


class AuthenticationProvider:

    PASSWORD_ABLE = True

    def authenticate(self, user, password: str, **kwargs) -> bool:
        raise NotImplementedError

    def generate_password(self, *args, **kwargs) -> (str, bytearray):
        if not self.is_password_able():
            raise NotPasswordAbleError(self.get_name())
        raise NotImplementedError

    @classmethod
    def is_password_able(cls):
        """check if auth needs an password"""
        return cls.PASSWORD_ABLE

    @classmethod
    def get_name(cls):
        return cls.__qualname__


class LocalAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        super(AuthenticationProvider, self).__init__()

    def authenticate(self, user, password: str, **kwargs) -> bool:
        from flask import current_app
        security_manager = current_app.manager_holder.get_security_manager()
        login_pass = security_manager.generate_hmac(password)
        if login_pass == user.get_password():
            return True
        raise WrongUserPasswordError(user.get_username())

    def generate_password(self):
        """TODO"""
        return "TEST"


class NoValidAuthenticationProviderError(Exception):
    """Exception if auth provider do not exist"""

    def __init__(self, authenticator):
        self.message = "The Provider {} is not a valid authentication-provider".format(authenticator)


class WrongUserPasswordError(Exception):
    """Exception if wrong user password"""

    def __init__(self, user):
        self.message = "The password for the user {} was wrong!".format(user)


class NotPasswordAbleError(Exception):
    """Exception if application tries to generate a password for an not password_able class"""

    def __init__(self, provider):
        self.message = "The AuthenticationProvider {} is not password able".format(provider)
