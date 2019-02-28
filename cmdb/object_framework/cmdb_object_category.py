from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.utils.error import CMDBError


class CmdbTypeCategory(CmdbDAO):
    """
    Type category
    """
    COLLECTION = 'objects.categories'
    REQUIRED_INIT_KEYS = [
        'name',
    ]

    def __init__(self, name: str, label: str = None, icon: str = None, type_list: list = None, parent_id=None,
                 **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.icon = icon or ''
        self.type_list = type_list or []
        self.parent_id = parent_id
        super(CmdbTypeCategory, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def get_icon(self) -> str:
        return self.icon

    def has_icon(self) -> bool:
        if self.icon:
            return True
        return False

    def get_types(self) -> list:
        return self.type_list

    def has_types(self) -> bool:
        if len(self.type_list) > 0:
            return True
        return False

    def get_parent(self) -> int:
        if self.parent_id is None:
            raise NoParentCategory(self.get_name())
        return self.parent_id

    def has_parent(self) -> bool:
        if self.parent_id is None:
            return False
        else:
            return True


class NoParentCategory(CMDBError):

    def __init__(self, name):
        super().__init__()
        self.message = 'The category {} has no parent element'.format(name)
