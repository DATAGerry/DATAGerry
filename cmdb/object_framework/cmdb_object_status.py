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

    def __init__(self, name: str, label: str, color: str, icon: str=None, **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.color = color
        self.icon = icon
        super(CmdbObjectStatus, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def get_color(self) -> str:
        return self.color

    def get_icon(self) -> str:
        return self.icon
