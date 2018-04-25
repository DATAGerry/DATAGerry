from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbType(CmdbDAO):
    """
    Definition of an object type - which fields were created and how.
    """
    COLLECTION = "objects.types"
    REQUIRED_INIT_KEYS = [
        'name',
        'title',
        'sections',
        'fields',
        'version'
    ]
    POSSIBLE_FIELD_TYPES = []

    def __init__(self, name, title, sections, fields, version, **kwargs):
        """
        init of cmdb type
        :param name: name of type
        :param title: title which is displayed
        :param sections: list of sections
        :param fields: list of fields
        :param version: version of type
        :param kwargs: additional data
        """
        self.name = name
        self.title = title
        self.sections = sections
        self.version = version
        self.fields = fields
        super(CmdbType, self).__init__(**kwargs)

    def get_name(self):
        """
        get name of type
        :return: type name
        """
        return self.name

    def get_title(self):
        """
        get title of type
        :return: type title
        """
        return self.title

    def get_sections(self):
        """
        get all sections
        :return: all sections
        """
        return self.sections

    def get_section(self, name):
        """
        get specific section
        :param name: name of section
        :return: chosen section
        """
        return self.sections[name]

    def get_fields(self):
        """
        get all fields
        :return: list of fields
        """
        return self.fields

    def get_field(self, name):
        """
        get specific field
        :param name: field name
        :return: field with value
        """
        for field in self.fields.items():
            if field.name == name:
                return field
        raise FieldNotFoundError(name, self.get_name())

    def get_version(self):
        """
        get version of type
        :return: current version
        """
        return self.version


class FieldNotFoundError(Exception):
    """
    Error if field do not exists
    """

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = 'Field {} was not found inside type: {}'.format(field_name, type_name)
