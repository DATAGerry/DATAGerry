from cmdb.object_framework.cmdb_dao import CmdbDAO, RequiredInitKeyNotFoundError
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType
from cmdb.utils.error import CMDBError
from datetime import datetime
from cmdb.utils import get_logger

LOGGER = get_logger()


class CmdbType(CmdbDAO):
    """
    Definition of an object type - which fields were created and how.
    """
    COLLECTION = "objects.types"
    REQUIRED_INIT_KEYS = [
        'name',
        'active',
        'author_id',
        'creation_time',
        'active',
        'render_meta',
    ]

    def __init__(self, name: str, description: str, active: bool, author_id: int, creation_time: datetime,
                 render_meta: list, fields: list, version: str = '1.0.0', label: str=None, status: list = None, logs: dict = None,
                 **kwargs):
        self.name = name
        self.label = label or self.name.title()
        self.description = description
        self.version = version
        self.status = status
        self.active = active
        self.author_id = author_id
        self.creation_time = creation_time
        self.render_meta = render_meta
        self.fields = fields or []
        self.logs = logs
        super(CmdbType, self).__init__(**kwargs)

    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def get_description(self):
        return self.description

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

    def get_section(self, name):
        try:
            return self.render_meta['sections'][name]
        except IndexError:
            return None

    def get_fields(self):

        return self.fields

    def get_field(self, name) -> CmdbFieldType:
        field = [x for x in self.fields if x['name'] == name]
        if field:
            try:
                return CmdbFieldType(**field[0])
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                LOGGER.warning(e.message)
                raise FieldInitError(name)
        raise FieldNotFoundError(name, self.get_name())


class FieldNotFoundError(CMDBError):
    """Error if field do not exists"""

    def __init__(self, field_name, type_name):
        super().__init__()
        self.message = 'Field {} was not found inside input_type: {}'.format(field_name, type_name)


class FieldInitError(CMDBError):
    """Error if field could not be initialized"""

    def __init__(self, field_name):
        super().__init__()
        self.message = 'Field {} could not be initialized: {}'.format(field_name)
