from cmdb.object_framework.cmdb_dao import CmdbDAO, RequiredInitKeyNotFoundError
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType, FieldNotFoundError
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

    def get_external(self, name):
        return self.render_meta['external'][name]

    def get_summaries(self):
        return self.render_meta['summary']

    def get_summary(self, name):
        for summary in self.render_meta['summary']:
            if summary['name'] == name:
                return summary
        return None

    def get_summary_fields(self, name):
        return self.get_summary(name)['fields']

    def get_sections(self):
        return sorted(self.render_meta['sections'], key=lambda k: k['position'])

    def get_section(self, name):
        try:
            return self.render_meta['sections'][name]
        except IndexError:
            return None

    def get_fields(self):

        return self.fields

    def get_field_of_type_with_value(self, input_type: str, _filter: str, value) -> CmdbFieldType:
        field = [x for x in self.fields if x['input_type'] == input_type and x[_filter] == value]
        if field:
            LOGGER.debug('Field of type {}'.format(input_type))
            LOGGER.debug('Field len'.format(field))
            LOGGER.debug('Field {}'.format(len(field)))
            try:
                return CmdbFieldType(**field[0])
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                LOGGER.warning(e.message)
                raise FieldInitError(value)
        else:
            LOGGER.debug('Field of type {} NOT found'.format(input_type))
            raise FieldNotFoundError(value, self.get_name())

    def get_field(self, name) -> CmdbFieldType:
        field = [x for x in self.fields if x['name'] == name]
        if field:
            try:
                return CmdbFieldType(**field[0])
            except (RequiredInitKeyNotFoundError, CMDBError) as e:
                LOGGER.warning(e.message)
                raise FieldInitError(name)
        raise FieldNotFoundError(name, self.get_name())


class FieldInitError(CMDBError):
    """Error if field could not be initialized"""

    def __init__(self, field_name):
        super().__init__()
        self.message = 'Field {} could not be initialized: {}'.format(field_name)
