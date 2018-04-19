# pylint: disable=useless-super-delegation
"""

"""

from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObject(CmdbDAO):
    """

    """

    COLLECTION = 'objects.data'
    REQUIRED_INIT_KEYS = []

    def __init__(self, *args, **kwargs):
        super(CmdbObject, self).__init__(*args, **kwargs)

    def get_all_values(self):
        pass

    def get_value(self, field):
        pass

    def get_author_id(self):
        if self.author:
            return self.author
        return None