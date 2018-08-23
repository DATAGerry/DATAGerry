from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbTypeCategory(CmdbDAO):
    """
    Type category
    """
    COLLECTION = 'objects.categories'
    REQUIRED_INIT_KEYS = [
        'name',
        'label'
    ]

    def __init__(self, name, label, parent_id=0, icon=None, type_list=[], **kwargs):
        self.name = name
        self.label = label
        self.parent_id = parent_id
        self.icon = icon
        self.type_list = type_list
        super(CmdbTypeCategory, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def get_parent_id(self) -> int:
        return self.parent_id

    def get_icon(self) -> str:
        return self.icon

    def has_icon(self) -> bool:
        if self.icon:
            return True
        return False

    def get_types(self) -> list:
        return self.type_list

    def is_empty(self) -> bool:
        if len(self.type_list) > 0:
            return False
        return True
