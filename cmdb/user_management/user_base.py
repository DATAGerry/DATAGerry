class UserManagementSetup:

    def setup(self):
        raise NotImplementedError

    @staticmethod
    def get_setup_data():
        raise NotImplementedError


class UserManagementBase:

    COLLECTION = 'management.*'
    SETUP_CLASS = UserManagementSetup

    def __new__(cls, *args, **kwargs):
        return super(UserManagementBase, cls).__new__(cls)

    def get_public_id(self):
        return self.public_id

    def to_database(self):
        return self.__dict__

    def to_mongo(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self):
        from cmdb.application_utils.program_utils import debug_print
        return debug_print(self)
