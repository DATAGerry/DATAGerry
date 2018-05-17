class UserManagementSetup:

    def setup(self):
        raise NotImplementedError

    @staticmethod
    def get_setup_data():
        raise NotImplementedError


class UserManagementBase:

    COLLECTION = 'management.*'
    SETUP_CLASS = UserManagementSetup

    def __init__(self, **kwargs):
        """
        init methode which auto convert params to the attribute dict
        :param kwargs: new generated attributes
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __new__(cls, *args, **kwargs):
        return super(UserManagementBase, cls).__new__(cls)

    def get_public_id(self):
        return self.public_id

    def to_database(self):
        return self.__dict__

    def to_mongo(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self):
        """
        Debug function for print tests
        :return: pretty formatted string
        """
        import pprint
        return 'Class: %s \nDict:\n%s' % \
               (self.__class__.__name__, pprint.pformat(self.__dict__))