from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbTypeCategory(CmdbDAO):
    """
    Type category
    """
    COLLECTION = 'objects.categories'
    REQUIRED_INIT_KEYS = [
        'name',
    ]

    def __init__(self, name: str, label: str=None, icon: str=None, type_list: list=None, children_list: list=None, **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.icon = icon or None
        self.type_list = type_list or []
        add_children = []
        if children_list is not None:
            for child in children_list:
                add_children.append(
                    CmdbTypeCategory(
                        **child
                    )
                )
                self.child_list = add_children
        else:
            self.child_list = children_list or []
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

    def has_children(self) -> bool:
        if len(self.child_list) > 0:
            return True
        return False

    def get_children(self) -> list:
        return self.child_list

    def get_types(self) -> list:
        return self.type_list

    def has_types(self) -> bool:
        if len(self.type_list) > 0:
            return True
        return False
