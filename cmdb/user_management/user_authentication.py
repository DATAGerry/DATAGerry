from cmdb.application_utils import SYSTEM_CONFIG_READER


class AuthenticationProvider:

    def __init__(self):
        self.settings = SYSTEM_CONFIG_READER.get_all_values_from_section('Authentication')
        self.security = SYSTEM_CONFIG_READER.get_all_values_from_section('Security')

    def authenticate(self, username, password):
        raise NotImplementedError


class LocalAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        from cmdb.data_storage import database_manager
        super().__init__()
        self.dbm = database_manager

    def authenticate(self, user, password):
        from cmdb.application_utils import SECURITY_MANAGER
        compare_hash = SECURITY_MANAGER.generate_hmac(password)
        if compare_hash == user.password:
            return True
        return False

"""
@deprecated
class LdapAuthenticationProvider(AuthenticationProvider):

    def __init__(self):
        super().__init__()
        self.ldap_server = self.settings['ldap_server']
        self.ldap_port = self.settings['ldap_port']
        self.ldap_ssl = eval(self.settings['ldap_ssl'])
        self.bind_dn = self.settings['bind_dn']
        self.base_dn = self.settings['base_dn']
        self.bind_password = self.settings['bind_password']
        self.search_filter = self.settings['search_filter']
        self.search_filter_sync = self.settings['search_filter_sync']

    def connect(self, bind_dn, password):
        from ldap3 import Server, Connection, ALL
        server = Server(host=self.ldap_server, port=int(self.ldap_port), use_ssl=self.ldap_ssl)
        conn = Connection(
            server=server,
            user=bind_dn,
            password=password,
            auto_bind=True)
        return conn

    def authenticate(self, user, password):
        connection = self.connect(bind_dn=self.bind_dn, password=self.bind_password)
        search_filter = self.search_filter.replace("%username%", user.user_name)
        connection.search(self.base_dn, search_filter, attributes='uid')
        user_dn = connection.entries[0].entry_dn
        try:
            self.connect(bind_dn=user_dn, password=password)
            return True
        except Exception:
            return False

    def sync_ldap(self):
        connection = self.connect(bind_dn=self.bind_dn, password=self.bind_password)
        connection.search(self.base_dn, self.search_filter_sync, attributes='uid')
        return connection.entries
"""