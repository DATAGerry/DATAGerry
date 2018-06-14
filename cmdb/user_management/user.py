from cmdb.user_management.user_base import UserManagementBase, UserManagementSetup
from cmdb.user_management.user_authentication import AuthenticationProvider, LocalAuthenticationProvider
from cmdb.user_management.user_exceptions import NoValidAuthenticationProvider


class UserSetup(UserManagementSetup):

    def setup(self):
        pass

    @staticmethod
    def get_setup_data():
       pass


class User(UserManagementBase):

    COLLECTION = 'management.users'
    SETUP_CLASS = UserSetup

    def __init__(self, public_id, user_name, group, registration_time, last_visit_time=None, password="",
                 first_name="", last_name="", authenticator=LocalAuthenticationProvider):
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

    @staticmethod
    def check_authenticator(authenticator):
        if issubclass(eval(authenticator), AuthenticationProvider):
            return authenticator
        else:
            raise NoValidAuthenticationProvider(authenticator)

    def set_password(self, new_password):
        self.password = new_password


