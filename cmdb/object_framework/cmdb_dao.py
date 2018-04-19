"""
Data Access Object for CMDB
"""


class CmdbDAO:
    """
    Data Access Object for CMDB
    """
    COLLECTION = 'objects.*'
    REQUIRED_INIT_KEYS = []
    VERSIONING_MAJOR = 1.0
    VERSIONING_MINOR = 0.1
    VERSIONING_PATCH = 0.01

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __new__(cls, *args, **kwargs):
        """
        @deprecated
        if not all(key in key_list for key in cls.REQUIRED_INIT_KEYS):
        raise InitKeyNotFoundError()
        """
        for r_key in cls.REQUIRED_INIT_KEYS:
            if r_key in kwargs:
                continue
            else:
                raise RequiredInitKeyNotFound(r_key)
        return super(CmdbDAO, cls).__new__(cls)

    @classmethod
    def _update_version(cls, current_version, update):
        import math
        if update == cls.VERSIONING_MINOR:
            return float(current_version) + float(update)
        elif update == cls.VERSIONING_MAJOR:
            return math.floor(current_version + update)
        return current_version + update

    def __repr__(self):
        """Debug function for print tests

        Returns: pretty formatted string
        """
        import pprint
        return 'Class: %s \nDict:\n%s' % \
               (self.__class__.__name__, pprint.pformat(self.__dict__))


class RequiredInitKeyNotFound(Exception):

    def __init__(self, key_name):
        super().__init__()
        self.message = 'Following initalisation key was not found inside the document: {}'.format(key_name)
