from cmdb.user_management.user_base import UserManagementBase
from cmdb.user_management.user_authentication import AuthenticationProvider
from cmdb.user_management.user_authentication import NoValidAuthenticationProviderError, LocalAuthenticationProvider
from cmdb.utils.error import CMDBError


class User(UserManagementBase):
    COLLECTION = 'management.users'

    INDEX_KEYS = [
        {'keys': [('user_name', UserManagementBase.DAO_ASCENDING)], 'user_name': 'user_name', 'unique': True}
    ]

    def __init__(self, user_name, group_id, registration_time, password=None,
                 first_name=None, last_name=None, email=None, authenticator='LocalAuthenticationProvider', **kwargs):
        self.user_name = user_name
        self.password = password
        self.group_id = group_id
        self.authenticator = authenticator
        if email is None or email == "":
            self.email = ""
        else:
            self.email = self.validate_email(email)
        self.registration_time = registration_time
        self.first_name = first_name
        self.last_name = last_name
        super(User, self).__init__(**kwargs)

    def get_name(self):
        if self.first_name is "" and self.last_name is "":
            return self.user_name
        else:
            return "{} {}".format(self.first_name, self.last_name)

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_username(self):
        return self.user_name

    def validate_email(self, address):
        if not self.is_valid_email(address):
            raise InvalidEmailError(address)
        return address

    def get_email(self):
        if self.email is None or self.email == "":
            return None
        return self.email

    @staticmethod
    def is_valid_email(email):
        import re
        if len(email) > 7:
            return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))

    def get_password(self):
        return self.password

    def get_group(self):
        return self.group_id

    def get_authenticator(self) -> AuthenticationProvider:
        if issubclass(eval(self.authenticator), AuthenticationProvider):
            return eval(self.authenticator)()
        else:
            raise NoValidAuthenticationProviderError(self.authenticator)


class InvalidEmailError(CMDBError):
    def __init__(self, address):
        self.message = 'Invalid email address: {}'.format(address)
