from cmdb.plugins.auth import AuthPluginBase
from cmdb.user_management.user_authentication import AuthenticationProvider


class ExamplePlugin(AuthPluginBase):

    def __init__(self):
        super(AuthPluginBase, 'auth_example_plugin', ExampleProvider)


class ExampleProvider(AuthenticationProvider):

    def __init__(self):
        super(AuthenticationProvider, self).__init__()

    def authenticate(self, user, password: str, **kwargs) -> bool:
        if user == 'admin':
            return True
        return False
