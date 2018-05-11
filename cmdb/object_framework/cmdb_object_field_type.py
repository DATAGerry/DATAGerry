from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbFieldType(CmdbDAO):
    """
    Presentation of a field type which is created within the Cmdb type.
    """
    COLLECTION = 'objects.fields'
    REQUIRED_INIT_KEYS = [
        'name',
        'label',
        'type',
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

    def __init__(self, **kwargs):
        """
        init of field types
        :param name: name of field type
        :param label: display label of name
        :param html_type: html type
        :param default: default value
        :param attributes: html attributes
        :param attr_data: optional data attributes
        :param kwargs: additional data
        """
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

    def get_type(self):
        """
        get chosen html type
        :return: html type
        """
        return self.type

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

    def get_html_output(self):
        if self.get_type() == 'text':
            return '<input type="text" class="form-control" id="{0}" name="{1}" />'.format(
                self.get_name(), self.get_name()
            )
        elif self.get_type() == 'password':
            return '<input type="password" class="form-control" id="{0}" name="{1}" />'.format(
                self.get_name(), self.get_name()
            )
        elif self.get_type() == 'textarea':
            return '<textarea class="form-control" rows="5" id="{0}" name="{1}"></textarea>'.format(
                self.get_name(), self.get_name()
            )
        elif self.get_type() == 'email':
            return '<input type="email" class="form-control" id="{0}" name="{1}" />'.format(
                self.get_name(), self.get_name()
            )
        elif self.get_type() == 'url':
            return '<input type="text" class="form-control" id="{0}" name="{1}" />'.format(
                self.get_name(), self.get_name()
            )
        elif self.get_type() == 'radio':
            output = ""
            for rad in self.possible_values:
                output += '<div class="form-check">' \
                       '<input class="form-check-input" type="radio" id="{0}" name="{1} "value="{2}">' \
                       '<label class="form-check-label" for="{3}">{4}</label></div>'.format(
                            rad, self.get_name(), rad, self.get_name(), rad)
            return output
        elif self.get_type() == 'range':
            return '<input type="range" class="form-control-range" id="{0}" name="{1}"" />'.format(
                self.get_name(), self.get_name()
            )
        return ""


class WrongHtmlType(Exception):
    """
    Error if html attribute is not in POSSIBLE_HTML_INPUT_TYPES list
    """

    def __init__(self, html_type):
        super().__init__()
        self.message = 'Wrong Html type {} - list of all posslible types {}'.format(
            html_type, CmdbFieldType.POSSIBLE_HTML_INPUT_TYPES
        )
