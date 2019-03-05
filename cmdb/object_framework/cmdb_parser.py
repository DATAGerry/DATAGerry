"""OBJECT Parser
"""
from cmdb.utils.error import CMDBError
from cmdb.object_framework import CmdbObject, CmdbType
from cmdb.object_framework.cmdb_object_field_type import CmdbFieldType
from cmdb.object_framework.cmdb_log import CmdbLog
from cmdb.utils.logger import get_logger

LOGGER = get_logger()


class CmdbParser:

    VIEW_MODE = 0
    EDIT_MODE = 1
    ADD_MODE = 2
    SHOW_MODE = 3

    DEFAULT_MODE = VIEW_MODE

    POSSIBLE_INPUT_FORM_TYPES = ['text', 'password', 'email', 'tel']
    POSSIBLE_RENDER_MODES = [ADD_MODE, VIEW_MODE, EDIT_MODE, SHOW_MODE]

    def __init__(self, type_instance: CmdbType, object_instance: CmdbObject = None, mode: int = DEFAULT_MODE):
        if mode not in CmdbParser.POSSIBLE_RENDER_MODES:
            raise RenderModeError()
        self.mode = mode
        self.type_instance = type_instance
        self.object_instance = object_instance

    def get_mode(self) -> int:
        return self.mode

    def has_external(self) -> bool:
        if len(self.type_instance.render_meta['external']) != 0:
            return True
        return False

    def has_summary(self) -> bool:
        if len(self.type_instance.render_meta['summary']) != 0:
            return True
        return False

    def all_externals_empty(self) -> bool:
        empty = True
        for external in self.type_instance.render_meta['external']:
            for field in external['fields']:
                field = self.object_instance.get_value(field)
                if field is not None:
                    empty = False
                    return empty
        return empty

    def load_external(self):
        if not self.has_external() or self.all_externals_empty():
            raise NoExternalDefined()
        return self.type_instance.render_meta['external']

    @property
    def object_instance(self) -> CmdbObject:
        return self._object_instance

    @object_instance.setter
    def object_instance(self, object_instance: CmdbObject):
        if self.mode == CmdbParser.ADD_MODE or self.mode == CmdbParser.SHOW_MODE:
            self._object_instance = None
        elif not isinstance(object_instance, CmdbObject):
            raise ObjectInstanceError()
        else:
            self._object_instance = object_instance

    @property
    def type_instance(self) -> CmdbType:
        return self._type_instance

    @type_instance.setter
    def type_instance(self, type_instance: CmdbType):
        if not isinstance(type_instance, CmdbType):
            raise TypeInstanceError()
        self._type_instance = type_instance

    def get_logs(self) -> (list, None):
        """
        TODO: Change in code to dao function
        Returns:

        """
        log_list = []
        for log in self.object_instance.get_logs():
            try:
                tmp_log = CmdbLog(**log)
                log_list.append(tmp_log)
            except CMDBError:
                continue
        return log_list

    def get_field(self, name):
        """
        TODO: Error handling
        """

        field = None
        if self.mode == CmdbParser.VIEW_MODE or self.mode == CmdbParser.EDIT_MODE:
            try:
                object_value = self.object_instance.get_value(name)
                if object_value is None or object_value == '':
                    return None
            except CMDBError:
                return None
            try:
                field = self.type_instance.get_field(name)
                object_value = self.object_instance.get_value(name)
                if object_value is not None or object_value != '':
                    enc_value = CmdbParser.field_encoder(field, object_value)
                    field.set_value(enc_value)
                return field
            except CMDBError:
                return None
        elif self.mode == CmdbParser.ADD_MODE or self.mode == CmdbParser.SHOW_MODE:
            try:
                field = self.type_instance.get_field(name)
                field.set_value(None)
                LOGGER.debug("Field: {}".format(field))
                return field
            except CMDBError:
                return None

        LOGGER.debug("OBJECTVALUE Field {}:".format(field))
        return field

    @staticmethod
    def field_encoder(field: CmdbFieldType, value):
        if field.get_type() == 'date':
            LOGGER.debug("Current field TYPE: {} | VALUE: {}".format(field.get_type(), value))
            try:
                str_date_value = value.strftime("%Y-%m-%d")
            except Exception:
                LOGGER.warning("Wrong data format in field {}".format(field))
                return value
            LOGGER.debug("Current field VALUE: {} | NEW VALUE: {}".format(value, str_date_value))
            return str_date_value
        return value

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class RenderModeError(CMDBError):
    def __init__(self):
        super(CMDBError, self)
        self.message = "No possible render mode"


class ObjectInstanceError(CMDBError):
    def __init__(self):
        super(CMDBError, self)
        self.message = "Wrong object instance"


class TypeInstanceError(CMDBError):
    def __init__(self):
        super(CMDBError, self)
        self.message = "Wrong type instance"


class NoExternalDefined(CMDBError):
    def __init__(self):
        super(CMDBError, self)
        self.message = "No external links are defined"


class InvalidHtmlInputType(CMDBError):
    def __init__(self, html_type):
        super(CMDBError, self)
        self.message = "Input type {} is not supported".format(html_type)
