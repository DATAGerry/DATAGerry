from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObjectStatus(CmdbDAO):

    COLLECTION = "objects.status"
    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'color'
    ]
    IGNORED_INIT_KEYS = [
        'public_id'
    ]
    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, **kwargs):
        self.name = name
        super(CmdbObjectStatus, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def get_color(self):
        return self.color

    def get_icon(self):
        return self.icon
