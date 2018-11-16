from cmdb.object_framework.cmdb_dao import CmdbDAO
from cmdb.object_framework.cmdb_log import CmdbLog
from cmdb.utils.error import CMDBError


class CmdbObject(CmdbDAO):
    """The CMDB object is the basic data wrapper for storing and holding the pure objects within the CMDB.
    """

    COLLECTION = 'objects.data'
    REQUIRED_INIT_KEYS = [
        'type_id',
        'version',
        'creation_time',
        'author_id',
        'last_edit_time',
        'active',
        'views',
        'fields'
    ]

    def __init__(self, type_id, status, creation_time, author_id, last_edit_time, active, fields, logs,
                 views: int = 0, version: str = '1.0.0', **kwargs):
        """init of object

        Args:
            type_id: public input_type id which implements the object
            version: current version of object
            creation_time: date of object creation
            author_id: public id of author
            last_edit_time: last date of editing
            active: object activation status
            views: numbers of views
            fields: data inside fields
            logs: object log
            **kwargs: additional data
        """
        self.type_id = type_id
        self.status = status
        self.version = version
        self.creation_time = creation_time
        self.author_id = author_id
        self.last_edit_time = last_edit_time
        self.active = active
        self.views = int(views)
        self.fields = fields
        self.logs = logs
        super(CmdbObject, self).__init__(**kwargs)

    def get_type_id(self) -> int:
        """get input_type if of this object

        Returns:
            int: public id of input_type

        """
        if self.type_id == 0 or self.type_id is None:
            raise TypeNotSetError(self.get_public_id())
        return self.type_id

    def update_view_counter(self) -> int:
        """update the number of times this object was viewed

        Returns:
            int: number of views

        """
        self.views += 1
        return self.views

    def get_all_fields(self) -> list:
        """ get all fields with key value pair

        Returns:
            all fields

        """

        return self.fields

    def get_value(self, field) -> str:
        """get value of an field

        Args:
            field: field_name

        Returns:
            value of field
        """
        for f in self.fields:
            if f['name'] == field:
                return f['value']
            continue
        return None

    def get_values(self, fields: list) -> list:
        list_of_values = []
        for field in self.fields:
            if field['name'] in fields:
                list_of_values.append(field['value'])
        return list_of_values

    def to_value_strings(self, field_names: list) -> str:
        value_string = ''
        for field_name in field_names:
            try:
                field_value = self.get_value(field_name)
                value_string += str(field_value)
                value_string += str(' ')
            except CMDBError:
                continue
        return value_string.strip()

    def empty_logs(self) -> bool:
        if len(self.logs) > 0:
            return True
        return False

    def log_length(self):
        return len(self.logs)-1

    def last_log(self):
        try:
            last_log = CmdbLog(**self.logs[-1])
        except CMDBError:
            return None
        return last_log


class TypeNotSetError(CMDBError):

    def __init__(self, public_id):
        super().__init__()
        self.message = 'The object (ID: {}) is not connected with a input_type'.format(public_id)


class NoLinksAvailableError(CMDBError):
    """
    @deprecated
    """

    def __init__(self, public_id):
        super().__init__()
        self.message = 'The object (ID: {}) has no links'.format(public_id)
