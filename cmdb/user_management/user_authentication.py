class AuthenticationProvider:

    def authenticate(self, username, password):
        raise NotImplementedError


class LocalAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        super(AuthenticationProvider, self).__init__()

    def authenticate(self, user, password):
        pass


class NoValidAuthenticationProviderError(Exception):
    """Exception if auth provider do not exist"""
    def __init__(self, authenticator):
        self.message = "The Provider {} is not a valid authentication-provider".format(authenticator)