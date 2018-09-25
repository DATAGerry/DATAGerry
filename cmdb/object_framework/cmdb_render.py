"""CMDB TYPE -> OBJECT RENDER
"""
from cmdb.utils.error import CMDBError
from cmdb.object_framework import CmdbObject, CmdbType, CmdbFieldType
from markupsafe import Markup
from cmdb.utils.logger import get_logger

LOGGER = get_logger()


class CmdbRender:

    VIEW_MODE = 0
    EDIT_MODE = 1

    POSSIBLE_FORM_TYPES = ['text', 'password', 'email']
    POSSIBLE_RENDER_MODES = [VIEW_MODE, EDIT_MODE]

    def __init__(self, object_instance: CmdbObject, type_instance: CmdbType):
        self.object_instance = object_instance
        self.type_instance = type_instance

    @property
    def object_instance(self) -> CmdbObject:
        return self._object_instance

    @object_instance.setter
    def object_instance(self, object_instance: CmdbObject):
        if not isinstance(object_instance, CmdbObject):
            raise ObjectInstanceError()
        self._object_instance = object_instance

    @property
    def type_instance(self) -> CmdbType:
        return self._type_instance

    @type_instance.setter
    def type_instance(self, type_instance: CmdbType):
        if not isinstance(type_instance, CmdbType):
            raise ObjectInstanceError()
        self._type_instance = type_instance

    def render_html_form(self, mode: int= VIEW_MODE):

        if mode not in CmdbRender.POSSIBLE_RENDER_MODES:
            raise RenderModeError()
        if mode == CmdbRender.VIEW_MODE:
            return self.render_html_form_view()
        elif mode == CmdbRender.EDIT_MODE:
            return self.render_html_form_edit()
        else:
            raise RenderModeError()

    def render_html_form_view(self):
        type_sections = self.type_instance.get_sections()
        html_code = ""
        for section in type_sections:
            html_code += '<h2>{}</h2><hr />'.format(section['label'])
            for field_name in section['fields']:
                try:
                    field_typ = self.type_instance.get_field(name=field_name)

                    html_code += self._render_html_input(field_typ)
                except CMDBError as e:
                    LOGGER.info(e.message)
                    continue

        return Markup(html_code)

    @staticmethod
    def _render_html_input(field_type: CmdbFieldType):
        html_type = field_type.get_sub_type()
        if html_type not in CmdbRender.POSSIBLE_FORM_TYPES:
            raise InvalidHtmlInputType(html_type)

        render_output = ''
        if field_type.get_type() == 'text':
            render_output += '<div class="form-group">'
            render_output += '<label for="{0}">{1}</label><input name="{0}" type="{2}" ' \
                             'class="form-control">'.format(
                field_type.name, field_type.label, field_type.get_sub_type())
            render_output += '</div>'

        return render_output

    def _render_html_text(self):
        pass

    def _render_html_textarea(self):
        pass


class RenderModeError(CMDBError):
    def __init__(self):
        super(CMDBError, self)
        self.message = "No possible render mode"



class ObjectInstanceError(CMDBError):
    def __init__(self):
        super(CMDBError, self)
        self.message = "Wrong instance"


class InvalidHtmlInputType(CMDBError):
    def __init__(self, html_type):
        super(CMDBError, self)
        self.message = "Input type {} is not supported".format(html_type)
