from cmdb.plugins.plugin_system import PluginBase
from cmdb.user_management.user_authentication import AuthenticationProvider, NoValidAuthenticationProviderError


class AuthPluginBase(PluginBase):

    def __init__(self, plugin_name: str, provider_class):
        if provider_class is not issubclass(AuthenticationProvider):
            raise NoValidAuthenticationProviderError(provider_class)
        self.provider_class = provider_class
        super(PluginBase, self).__init__(plugin_name, 'auth')

    def get_provider_class(self):
        return self.provider_class
