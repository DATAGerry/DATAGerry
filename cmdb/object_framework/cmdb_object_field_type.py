from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbFieldType(CmdbDAO):
    """
    Presentation of a field type which is created within the Cmdb type.
    """
    COLLECTION = 'objects.fields'
    REQUIRED_INIT_KEYS = [
        'name',
        'html_type',
        'default',
        'attributes',
    ]
    POSSIBLE_HTML_INPUT_TYPES = [
        'text',
        'password',
        'radio',
        'checkbox',
        'select',
        'color',
        'file',
        'date',
        'time',
        'datetime-local',
        'number',
        'email',
        'url',
        'range',
        'textarea'
    ]

    def __init__(self, name, html_type, default, attributes, attr_data=None, **kwargs):
        """
        init of field types
        :param name: name of field type
        :param html_type: html type
        :param default: default value
        :param attributes: html attributes
        :param attr_data: optional data attributes
        :param kwargs: additional data
        """
        self.name = name
        self.html_type = self._check_html_type(html_type)
        self.default = default
        self.attributes = attributes
        self.attr_data = attr_data
        super(CmdbFieldType, self).__init__(**kwargs)

    @classmethod
    def _check_html_type(cls, type_name):
        """
        check if html type is possible
        :param type_name: type name
        :return: True/False
        """
        if type_name not in cls.POSSIBLE_HTML_INPUT_TYPES:
            raise WrongHtmlType(type_name)
        return type_name

    def get_name(self):
        """
        get name of field type
        :return: name
        """
        return self.name

    def get_html_type(self):
        """
        get chosen html type
        :return: html type
        """
        return self.html_type

    def get_default_value(self):
        """
        get default html value
        :return: default value
        """
        return self.default

    def get_attributes(self):
        """
        get list of all attributes
        :return: attribute list
        """
        return self.attributes

    def get_attribute(self, name):
        """
        get specific attribute
        :param name: name of attribute
        :return: selected attribute
        """
        return self.attributes[name]


class WrongHtmlType(Exception):
    """
    Error if html attribute is not in POSSIBLE_HTML_INPUT_TYPES list
    """

    def __init__(self, html_type):
        super().__init__()
        self.message = 'Wrong Html type {} - list of all posslible types {}'.format(
            html_type, CmdbFieldType.POSSIBLE_HTML_INPUT_TYPES
        )
