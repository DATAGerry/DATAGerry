from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbFieldType(CmdbDAO):
    """
    Presentation of a field input_type which is created within the Cmdb input_type.
    """
    COLLECTION = 'objects.types[fields]'  # Not used - implemented into type class

    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'input_type',
    ]
    IGNORED_INIT_KEYS = [
        'public_id'
    ]
    INDEX_KEYS = [
        # {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, input_type: str, name: str, label: str = None, description: str = None, placeholder: str = None,
                 values: list = None, roles: list = None, subtype: str = None, maxlength: int = None,
                 required: bool = False, access: bool = False,
                 className: str = 'form-control', **kwargs):
        self.value = None
        self.input_type = input_type
        self.subinput_type = subtype
        self.name = name
        self.label = label or name.title()
        self.description = description
        self.placeholder = placeholder
        self.className = className
        self.values = values or []
        self.roles = roles or []
        self.maxlength = maxlength
        self.required = required
        self.access = access
        super(CmdbFieldType, self).__init__(**kwargs)

    def get_value(self):
        return self.value

    def get_type(self):
        return self.input_type

    def get_sub_type(self):
        if self.subinput_type is None:
            return self.input_type
        return self.subinput_type

    def is_protected(self):
        return self.access
