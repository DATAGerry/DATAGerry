from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbFieldType(CmdbDAO):
    """
    Presentation of a field type which is created within the Cmdb type.
    """
    COLLECTION = 'objects.types.fields'
    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'type',
    ]
    IGNORED_INIT_KEYS = [
        'public_id'
    ]
    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, type: str, subtype: str, name: str, label: str, description: str = None, placeholder: str = None,
                 values: list = [], roles: list = [], maxlength: int = None, required: bool = False, access: bool = False,
                 className: str = 'form-control', **kwargs):
        self.value = None
        self.type = type
        self.subtype = subtype
        self.name = name
        self.label = label
        self.description = description
        self.placeholder = placeholder
        self.className = className
        self.values = values
        self.roles = roles
        self.maxlength = maxlength
        self.required = required
        self.access = access
        super(CmdbFieldType, self).__init__(**kwargs)

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def get_sub_type(self):
        return self.subtype

    def is_protected(self):
        return self.access

    def render_html(self):
        return NotImplemented
