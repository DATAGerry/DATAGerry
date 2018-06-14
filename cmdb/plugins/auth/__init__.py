from cmdb.plugins.plugin_base import PluginType
from cmdb.user_management.user_authentication import AuthenticationProvider


class PluginAuthBase(AuthenticationProvider, metaclass=PluginType):

    def __init__(self, requirements=None):
        self.requirements = requirements or 'requirements.txt'

    def authenticate(self, username, password) -> bool:
        raise NotImplementedError
