from cmdb.user_management.user_base import UserManagementBase
from cmdb.user_management.user_authentication import AuthenticationProvider, LocalAuthenticationProvider
from cmdb.user_management.user_authentication import NoValidAuthenticationProviderError


class User(UserManagementBase):

    COLLECTION = 'management.users'

    INDEX_KEYS = [
        {'keys': [('user_name', UserManagementBase.DAO_ASCENDING)], 'user_name': 'user_name', 'unique': True}
    ]

    def __init__(self, public_id, user_name, group_id, registration_time, password=None,
                 first_name=None, last_name=None, email=None, authenticator='LocalAuthenticationProvider', **kwargs):
        self.public_id = public_id
        self.user_name = user_name
        self.password = password
        self.group_id = group_id
        self.authenticator = authenticator
        self.email = email
        self.registration_time = registration_time
        self.first_name = first_name
        self.last_name = last_name
        super(User, self).__init__(**kwargs)

    def get_username(self):
        return self.user_name

    def get_authenticator(self):
        if issubclass(eval(self.authenticator), AuthenticationProvider):
            return eval(self.authenticator)
        else:
            raise NoValidAuthenticationProviderError(self.authenticator)
