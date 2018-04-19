from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbType(CmdbDAO):

    COLLECTION = "objects.types"
    REQUIRED_INIT_KEYS = []
    POSSIBLE_FIELD_TYPES = []

    def __init__(self, *args, **kwargs):
        super(CmdbType, self).__init__(*args, **kwargs)

    def get_sections(self):
        pass

    def get_section(self, name):
        pass

    def get_title(self):
        return self.title

    def get_version(self):
        return self.version