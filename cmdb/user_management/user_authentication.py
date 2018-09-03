from cmdb.utils import get_logger
CMDB_LOGGER = get_logger()


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
        CMDB_LOGGER.info("Wrong password")
        return False


class NoValidAuthenticationProviderError(Exception):
    """Exception if auth provider do not exist"""
    def __init__(self, authenticator):
        self.message = "The Provider {} is not a valid authentication-provider".format(authenticator)