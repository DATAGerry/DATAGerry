from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbFieldType(CmdbDAO):

    COLLECTION = 'objects.fields'
    REQUIRED_INIT_KEYS = ['name', 'default']

    def __init__(self, *args, **kwargs):
        super(CmdbFieldType, self).__init__(*args, **kwargs)

