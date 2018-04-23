class UserManagementSetup:
    """
    setup superclass
    required for auto-setup
    """

    def __init__(self):
        from cmdb.data_storage import database_manager
        self.dbm = database_manager

    def setup(self):
        """
        hook call method from core routine

        Returns: NotImplementedError
        """
        raise NotImplementedError

    @staticmethod
    def get_setup_data():
        """
        static init data for user specific system

        Returns: NotImplementedError
        """
        raise NotImplementedError


class UserManagementBase:
    """
    user management superclass

    Attributes:
        COLLECTION (str):   "TABLE" Name of the database which
                            holds the cmdb objects
        SETUP_CLASS (str):  "Associated setup class"
    """

    COLLECTION = 'management.*'
    SETUP_CLASS = UserManagementSetup

    def to_mongo(self):
        """
        Fast workaround for converting objects for the Mongodb

        Returns (str): returns __dict__ structure of the object without None values
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}


