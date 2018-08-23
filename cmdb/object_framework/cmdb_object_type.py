from cmdb.object_framework.cmdb_dao import CmdbDAO, RequiredInitKeyNotFoundError
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType


class CmdbType(CmdbDAO):
    """
    Definition of an object type - which fields were created and how.
    """
    COLLECTION = "objects.types"
    SCHEMA = "type.schema.json"
    REQUIRED_INIT_KEYS = [
        'name',
        'version'
    ]
    POSSIBLE_FIELD_TYPES = []

    def __init__(self, name: str, title: str, description: str, version: str, status: list,
                 active: bool, creator_id: int, creation_time, render_meta: list, fields: list,
                 last_editor_id: int=0, last_edit_time=None, **kwargs):
        self.name = name
        self.title = title
        self.description = description
        self.version = version
        self.status = status
        self.active = active
        self.creator_id = creator_id
        self.creation_time = creation_time
        self.last_editor_id = last_editor_id
        self.last_edit_time = last_edit_time
        self.render_meta = render_meta
        self.fields = fields
        super(CmdbType, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_externals(self):
        return self.render_meta['external']

    def get_external(self, _id):
        try:
            return self.render_meta['external'][_id]
        except IndexError:
            return None

    def get_summaries(self):
        return self.render_meta['summary']

    def get_summary(self, _id):
        try:
            return self.render_meta['summary'][_id]
        except IndexError:
            return None

    def get_sections(self):
        return sorted(self.render_meta['sections'], key=lambda k: k['position'])

    def get_section(self, _id):
        try:
            return self.render_meta['sections'][_id]
        except IndexError:
            return None

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
        for field in self.fields:
            if field['name'] == name:
                try:
                    return CmdbFieldType(**field)
                except RequiredInitKeyNotFoundError as e:
                    print(e.message)
                    return None
        raise FieldNotFoundError(name, self.get_name())


class FieldNotFoundError(Exception):
    """
    Error if field do not exists
    """

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = 'Field {} was not found inside type: {}'.format(field_name, type_name)
