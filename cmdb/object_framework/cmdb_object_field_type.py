from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbFieldType(CmdbDAO):
    """
    Presentation of a field type which is created within the Cmdb type.
    """
    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'type',
    ]
    IGNORED_INIT_KEYS = [
        'public_id'
    ]

    def __init__(self, type: str, subtype: str, name: str, label: str, description: str = None, placeholder: str = None,
                 values: list = [], role: list = [], maxlength: int = None, required: bool = False, access: bool = False,
                 className: str = 'form-control', public_id: int = -1, **kwargs):
        self.public_id = public_id
        self.value = None
        self.type = type
        self.subtype = subtype
        self.name = name
        self.label = label
        self.description = description
        self.placeholder = placeholder
        self.className = className
        self.values = values
        self.role = role
        self.maxlength = maxlength
        self.required = required
        self.access = access
        super(CmdbFieldType, self).__init__(**kwargs)

    def set_value(self, val):
        self.value = val

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
