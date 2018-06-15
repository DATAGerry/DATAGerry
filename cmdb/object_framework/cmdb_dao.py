class CmdbDAO:
    """
    The data access object is the basic presentation if objects and
    their necessary dependent classes are to be stored in the database.
    """

    COLLECTION = 'objects.*'
    _SUPER_INIT_KEYS = [
        'public_id'
    ]
    IGNORED_INIT_KEYS = []
    REQUIRED_INIT_KEYS = []
    VERSIONING_MAJOR = 1.0
    VERSIONING_MINOR = 0.1
    VERSIONING_PATCH = 0.01

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_public_id(self) -> int:
        """
        get the public id of current element

        Note:
            Since the dao object is not initializable
            the child class object will inherit this function
            SHOULD NOT BE OVERWRITTEN!

        Returns:
            int: public id

        """
        return self.public_id

    def has_object_id(self):
        """

        Returns:

        """
        if hasattr(self, '_id'):
            return True
        else:
            return False

    def __new__(cls, *args, **kwargs):
        """
        @deprecated_implementation
        if not all(key in key_list for key in cls.REQUIRED_INIT_KEYS):
        raise InitKeyNotFoundError()
        """
        init_keys = cls._SUPER_INIT_KEYS + cls.REQUIRED_INIT_KEYS
        if len(cls.IGNORED_INIT_KEYS) > 0:
            init_keys = [i for j, i in enumerate(init_keys) if j in cls.IGNORED_INIT_KEYS]
        for req_key in init_keys:
            if req_key in kwargs:
                continue
            else:
                raise RequiredInitKeyNotFound(req_key)
        return super(CmdbDAO, cls).__new__(cls)

    def _update_version(self, update):
        """
        updates the version based on versioning
        :param update: update step
        :return: new version
        """
        import math
        if update == self.VERSIONING_MINOR:
            return float(self.version) + float(update)
        elif update == self.VERSIONING_MAJOR:
            return math.floor(self.version + update)
        return self.version + update

    def __repr__(self):
        from cmdb.application_utils.program_utils import debug_print
        return debug_print(self)

    def to_database(self):
        return self.__dict__

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class RequiredInitKeyNotFound(Exception):
    """
    Error if on of the given parameters is missing inside required init keys
    """

    def __init__(self, key_name):
        super().__init__()
        self.message = 'Following initalisation key was not found inside the document: {}'.format(key_name)
