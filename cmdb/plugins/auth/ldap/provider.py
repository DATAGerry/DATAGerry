from cmdb.plugins.auth import AuthPluginBase
from cmdb.user_management.user_authentication import AuthenticationProvider


class LDAPAuthenticationPlugin(AuthPluginBase):

    def __init__(self):
        super(AuthPluginBase, 'LDAPAuthenticationProvider', LdapAuthenticationProvider)


class LdapAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        from cmdb.utils import get_system_settings_reader
        self.settings = get_system_settings_reader()

        self.ldap_server = self.settings.get_value('ldap_server', 'ldap_plugin')
        self.ldap_port = self.settings.get_value('ldap_port', 'ldap_plugin')
        self.ldap_ssl = eval(self.settings.get_value('ldap_ssl', 'ldap_plugin'))
        self.bind_dn = self.settings.get_value('bind_dn', 'ldap_plugin')
        self.base_dn = self.settings.get_value('base_dn', 'ldap_plugin')
        self.bind_password = self.settings.get_value('bind_password', 'ldap_plugin')
        self.search_filter = self.settings.get_value('search_filter', 'ldap_plugin')
        self.search_filter_sync = self.settings.get_value('search_filter_sync', 'ldap_plugin')
        super(AuthenticationProvider, self).__init__()

    def connect(self, bind_dn, password):
        from ldap3 import Server, Connection
        server = Server(host=self.ldap_server, port=int(self.ldap_port), use_ssl=self.ldap_ssl)
        conn = Connection(
            server=server,
            user=bind_dn,
            password=password,
            auto_bind=True)
        return conn

    def authenticate(self, user, password: str, **kwargs) -> bool:
        connection = self.connect(bind_dn=self.bind_dn, password=self.bind_password)
        search_filter = self.search_filter.replace("%username%", user.user_name)
        connection.search(self.base_dn, search_filter, attributes='uid')
        user_dn = connection.entries[0].entry_dn
        try:
            self.connect(bind_dn=user_dn, password=password)
            return True
        except Exception:
            return False
