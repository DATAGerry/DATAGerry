from cmdb.object_framework.cmdb_dao import CmdbDAO
from typing import Tuple, List


class CmdbCollection(CmdbDAO):

    COLLECTION = "objects.collection"
    REQUIRED_INIT_KEYS = [
        'template_id',
        'user_id'
    ]

    def __init__(self, template_id: int, user_id: int, **kwargs):
        self.template_id = template_id
        self.user_id = user_id
        super(CmdbCollection, self).__init__(**kwargs)

    def get_template_id(self) -> int:
        return self.template_id


class CmdbCollectionTemplates(CmdbDAO):

    COLLECTION = "objects.collection.template"
    REQUIRED_INIT_KEYS = [
        'name',
        'user_id'
    ]
    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]
    TYPE_TUPLE = Tuple[int, int]

    def __init__(self, name: str, user_id: int, type_list: List[TYPE_TUPLE]=None, label: str=None, **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.user_id = user_id
        self.type_list = type_list or []
        super(CmdbCollectionTemplates, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def get_user_id(self) -> int:
        return self.user_id

    @staticmethod
    def get_type_tuple_from(type_id, count) -> TYPE_TUPLE:
        return type_id, count
