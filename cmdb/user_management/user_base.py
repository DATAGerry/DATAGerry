import logging

from cmdb.object_framework.cmdb_dao import NoPublicIDError, RequiredInitKeyNotFoundError
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


class UserManagementBase:
    ASCENDING = 1
    DESCENDING = -1
    COLLECTION = 'management.*'
    __SUPER_INIT_KEYS = [
        'public_id'
    ]
    __SUPER_INDEX_KEYS = [
        {'keys': [('public_id', ASCENDING)], 'name': 'public_id', 'unique': True}
    ]
    IGNORED_INIT_KEYS = []
    REQUIRED_INIT_KEYS = []
    INDEX_KEYS = []

    def __init__(self, **kwargs):
        self.public_id = None
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __new__(cls, *args, **kwargs):
        init_keys = cls.__SUPER_INIT_KEYS + cls.REQUIRED_INIT_KEYS
        if len(cls.IGNORED_INIT_KEYS) > 0:
            init_keys = [i for j, i in enumerate(init_keys) if j in cls.IGNORED_INIT_KEYS]
        for req_key in init_keys:
            if req_key in kwargs:
                continue
            else:
                raise RequiredInitKeyNotFoundError(req_key)
        return super(UserManagementBase, cls).__new__(cls)

    def get_public_id(self) -> int:
        if self.public_id == 0 or self.public_id is None:
            raise NoUserIDError(self.public_id)
        return self.public_id

    def to_json(self) -> dict:
        """
        converts attribute dict to json - maybe later for database updates
        Returns:
            dict: json dump with database default encoding of the object attributes
        """
        from cmdb.data_storage.database_utils import default
        import json
        return json.dumps(self.__dict__, default=default)


class NoUserIDError(NoPublicIDError):

    def __init__(self, user_id=None):
        self.message = f'User ID not set - UserID: {user_id}'
        super(NoPublicIDError, self).__init__(self.message)
