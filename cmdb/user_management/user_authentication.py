import logging
CMDB_LOGGER = logging.getLogger(__name__)


class AuthenticationProvider:

    def authenticate(self, user, password: str, **kwargs) -> bool:
        raise NotImplementedError


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


class NoValidAuthenticationProviderError(Exception):
    """Exception if auth provider do not exist"""
    def __init__(self, authenticator):
        self.message = "The Provider {} is not a valid authentication-provider".format(authenticator)


class WrongUserPasswordError(Exception):
    """Exception if wrong user password"""
    def __init__(self, user):
        self.message = "The password for the user {} was wrong!".format(user)
