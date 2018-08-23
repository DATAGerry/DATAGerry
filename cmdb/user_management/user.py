from cmdb.user_management.user_base import UserManagementBase
from cmdb.user_management.user_authentication import AuthenticationProvider, LocalAuthenticationProvider
from cmdb.user_management.user_authentication import NoValidAuthenticationProviderError


class User(UserManagementBase):

    COLLECTION = 'management.users'

    def __init__(self, public_id, user_name, group, registration_time, last_visit_time=None, password=None,
                 first_name=None, last_name=None, authenticator=LocalAuthenticationProvider):
        self.public_id = public_id
        self.user_name = user_name
        self.password = password
        self.group = group
        self.authenticator = authenticator
        self.registration_time = registration_time
        self.last_visit_time = last_visit_time
        self.first_name = first_name
        self.last_name = last_name
        super(User, self).__init__()

    def get_authenticator(self):
        if issubclass(self.authenticator, AuthenticationProvider):
            return self.authenticator
        else:
            raise NoValidAuthenticationProviderError(self.authenticator)
