from cmdb.user_management.user_dao import UserManagementBase, UserManagementSetup
from cmdb.user_management.user_authentication import *
from cmdb.user_management.user_exceptions import NoValidAuthenticationProvider


class UserSetup(UserManagementSetup):
    """

    """

    def setup(self):
        return self.dbm.insert(UserSetup.get_setup_data().to_mongo(), User.COLLECTION)

    @staticmethod
    def get_setup_data():
        from cmdb.application.security.security_manager import hmac_sha256
        from cmdb.application import system_config_reader
        from datetime import datetime
        admin_pass = hmac_sha256(system_config_reader.get_value('secret_key', 'Security'),
                                    'admin' + system_config_reader.get_value('password_salt', 'Security'))
        return User(
            public_id=0,
            user_name='admin',
            password=admin_pass,
            authenticator='LocalAuthenticationProvider',
            group='admin',
            registration_time=datetime.utcnow(),
        )


class User(UserManagementBase):

    COLLECTION = 'management.users'
    SETUP_CLASS = UserSetup

    def __init__(self, public_id, user_name, authenticator, group, password="", *args, **kwargs):
        self.public_id = public_id
        self.user_name = user_name
        self.password = password
        self.group = group
        try:
            self.authenticator = self.check_authenticator(authenticator)
        except NoValidAuthenticationProvider:
            self.authenticator = LocalAuthenticationProvider
        self.__dict__.update(kwargs)

    @staticmethod
    def check_authenticator(authenticator):
        if issubclass(eval(authenticator), AuthenticationProvider):
            return authenticator
        else:
            raise NoValidAuthenticationProvider(authenticator)

    def set_password(self, new_password):
        self.password = new_password


