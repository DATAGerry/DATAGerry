from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbTypeCategory(CmdbDAO):

    COLLECTION = "objects.types.categories"
    REQUIRED_INIT_KEYS = []
    POSSIBLE_FIELD_TYPES = []

    def __init__(self, *args, **kwargs):
        super(CmdbTypeCategory, self).__init__(*args, **kwargs)
