from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbStatus(CmdbDAO):

    COLLECTION = "objects.status"
    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'color'
    ]

    def __init__(self, public_id: int, name: str, label: str, color: str, icon: str=None, **kwargs):
        self.public_id = public_id
        self.name = name
        self.label = label
        self.color = color
        self.icon = icon
        super(CmdbStatus, self).__init__(**kwargs)

    def get_name(self):
        """
        get name of category
        :return: category name
        """
        return self.name

    def get_label(self):
        return self.label

    def get_icon(self):
        return self.icon
