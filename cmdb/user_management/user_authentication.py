class AuthenticationProvider:

    def __init__(self):
        pass

    def authenticate(self, username, password):
        raise NotImplementedError


class LocalAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        super().__init__()

    def authenticate(self, user, password):
        pass