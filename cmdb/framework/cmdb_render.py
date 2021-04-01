# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Object/Type render
"""

import logging
from typing import List, Union

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework.cmdb_errors import ObjectManagerGetError, TypeReferenceLineFillError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.security.acl.errors import AccessDeniedError
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.utils.wraps import timing

from cmdb.utils.error import CMDBError

from datetime import datetime

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.models.type import TypeModel, TypeExternalLink, TypeFieldSection, TypeReference, \
    TypeReferenceSection
from cmdb.user_management.user_manager import UserModel
from cmdb.user_management.managers.user_manager import UserManager
from dateutil.parser import parse

LOGGER = logging.getLogger(__name__)


class RenderVisualization:

    def __init__(self):
        self.current_render_time = datetime.now()
        self.object_information: dict = {}
        self.type_information: dict = {}

    def get_object_information(self, idx):
        return self.object_information[idx]

    def get_type_information(self, idx):
        return self.type_information[idx]


class RenderResult(RenderVisualization):

    def __init__(self):
        super(RenderResult, self).__init__()
        self.fields: list = []
        self.sections: list = []
        self.summaries: list = []
        self.summary_line: str = ''
        self.externals: list = []


class CmdbRender:
    AUTHOR_ANONYMOUS_NAME = 'unknown'

    def __init__(self, object_instance: CmdbObject,
                 type_instance: TypeModel,
                 render_user: UserModel,
                 object_manager: CmdbObjectManager = None, ref_render=False):
        self.object_instance: CmdbObject = object_instance
        self.type_instance: TypeModel = type_instance
        self.render_user: UserModel = render_user

        self.object_manager = object_manager
        if self.object_manager:  # TODO: Refactor to pass database-manager in init
            self.type_manager = TypeManager(self.object_manager.dbm)
            self.user_manager = UserManager(self.object_manager.dbm)

        self.ref_render = ref_render

    @property
    def object_instance(self) -> CmdbObject:
        """
        Object of the class CmdbObject that has already been instantiated.
        The data should come from the database and already be validated.
        This already happens when the object is instantiated.
        """
        return self._object_instance

    @object_instance.setter
    def object_instance(self, object_instance: CmdbObject):
        """
        Property setter for object_instance. The render only checks whether the passed object
        belongs to the correct class, not whether it is valid.
        """
        if not isinstance(object_instance, CmdbObject):
            raise ObjectInstanceError()
        else:
            self._object_instance = object_instance

    @property
    def type_instance(self) -> TypeModel:
        """
        Object of the class TypeModel that has already been instantiated.
        The data should come from the database and already be validated.
        This already happens when the object is instantiated.
        """
        return self._type_instance

    @type_instance.setter
    def type_instance(self, type_instance: TypeModel):
        """
        Property setter for type_instance. The render only checks whether the passed object
        belongs to the correct class, not whether it is valid.
        """
        if not isinstance(type_instance, TypeModel):
            raise TypeInstanceError()
        self._type_instance = type_instance

    def result(self) -> RenderResult:
        return self._generate_result()

    def _generate_result(self) -> RenderResult:
        render_result = RenderResult()
        try:
            render_result = self.__generate_object_information(render_result)
            render_result = self.__generate_type_information(render_result)
            render_result = self.__set_fields(render_result)
            render_result = self.__set_sections(render_result)
            render_result = self.__set_summaries(render_result)
            render_result = self.__set_external(render_result)
        except CMDBError as err:
            import traceback
            traceback.print_exc()
            raise RenderError(f'Error while generating a CMDBResult: {str(err)}')
        return render_result

    def __generate_object_information(self, render_result: RenderResult) -> RenderResult:
        try:
            author_name = self.user_manager.get(self.object_instance.author_id).get_display_name()
        except CMDBError:
            author_name = CmdbRender.AUTHOR_ANONYMOUS_NAME

        if self.object_instance.editor_id:
            try:
                editor_name = self.user_manager.get(self.object_instance.editor_id).get_display_name()
            except CMDBError:
                editor_name = None
        else:
            editor_name = None

        render_result.object_information = {
            'object_id': self.object_instance.public_id,
            'creation_time': self.object_instance.creation_time,
            'last_edit_time': self.object_instance.last_edit_time,
            'author_id': self.object_instance.author_id,
            'author_name': author_name,
            'editor_id': self.object_instance.editor_id,
            'editor_name': editor_name,
            'active': self.object_instance.active,
            'version': self.object_instance.version
        }
        return render_result

    def __generate_type_information(self, render_result: RenderResult) -> RenderResult:
        try:
            author_name = self.user_manager.get(self.type_instance.author_id).get_display_name()
        except CMDBError as err:
            author_name = CmdbRender.AUTHOR_ANONYMOUS_NAME
        try:
            self.type_instance.render_meta.icon
        except KeyError:
            self.type_instance.render_meta.icon = ''
        render_result.type_information = {
            'type_id': self.type_instance.public_id,
            'type_name': self.type_instance.name,
            'type_label': self.type_instance.label,
            'creation_time': self.type_instance.creation_time,
            'author_id': self.type_instance.author_id,
            'author_name': author_name,
            'icon': self.type_instance.render_meta.icon,
            'active': self.type_instance.active,
            'version': self.type_instance.version,
            'acl': self.type_instance.acl.to_json(self.type_instance.acl)

        }
        return render_result

    def __set_fields(self, render_result: RenderResult) -> RenderResult:
        render_result.fields = self.__merge_fields_value()
        return render_result

    def __set_sections(self, render_result: RenderResult) -> RenderResult:
        try:
            render_result.sections = [section.to_json(section) for section in
                                      self.type_instance.render_meta.sections]
        except (IndexError, ValueError):
            render_result.sections = []
        return render_result

    def __merge_field_content_section(self, field: dict, object_: CmdbObject):
        curr_field = [x for x in object_.fields if x['name'] == field['name']][0]
        if curr_field['name'] == field['name'] and field.get('value'):
            field['default'] = field['value']
        field['value'] = curr_field['value']
        # handle dates that are stored as strings
        if field['type'] == 'date' and isinstance(field['value'], str) and field['value']:
            field['value'] = parse(field['value'], fuzzy=True)

        if self.ref_render and field['type'] == 'ref' and field['value']:
            field['reference'] = self.__merge_references(field)
        return field

    def __merge_fields_value(self) -> List[dict]:
        field_map = []
        for idx, section in enumerate(self.type_instance.render_meta.sections):
            if type(section) is TypeFieldSection and isinstance(section, TypeFieldSection):
                for section_field in section.fields:
                    field = {}
                    try:
                        type_field = self.type_instance.get_field(section_field)

                        field = self.__merge_field_content_section(type_field, self.object_instance)
                    except FileNotFoundError:
                        LOGGER.error(f'Could not find field: {section_field}')
                        continue
                    except (ValueError, IndexError) as e:
                        LOGGER.error(f'Could not merge field: {str(e)}')
                        field['value'] = None
                    field_map.append(field)
            elif type(section) is TypeReferenceSection and isinstance(section, TypeReferenceSection):
                ref_field_name: str = f'{section.name}-field'
                ref_field = self.type_instance.get_field(ref_field_name)
                reference_id: int = self.object_instance.get_value(ref_field_name)
                ref_field['value'] = reference_id
                reference_object: CmdbObject = self.object_manager.get_object(public_id=reference_id)
                ref_type: TypeModel = self.type_manager.get(section.reference.type_id)
                ref_section = ref_type.get_section(section.reference.section_name)
                ref_field['references'] = {
                    'type_id': ref_type.public_id,
                    'type_name': ref_type.name,
                    'type_label': ref_type.label,
                    'fields': []
                }
                if not ref_section:
                    continue
                if not section.reference.selected_fields or len(section.reference.selected_fields) == 0:
                    selected_ref_fields = ref_section.fields
                    section.reference.selected_fields = selected_ref_fields
                    self.type_instance.render_meta.sections[idx] = section
                else:
                    selected_ref_fields = [f for f in ref_section.fields if f in section.reference.selected_fields]
                for ref_section_field_name in selected_ref_fields:
                    ref_section_field = ref_type.get_field(ref_section_field_name)
                    try:
                        field = self.__merge_field_content_section(ref_section_field, reference_object)
                    except (FileNotFoundError, ValueError, IndexError):
                        continue
                    ref_field['references']['fields'].append(field)
                field_map.append(ref_field)
        return field_map

    def __merge_references(self, current_field):

        # Initialise TypeReference
        reference = TypeReference(type_id=0, label='', line='')

        if current_field['value']:
            try:
                ref_object = self.object_manager.get_object(int(current_field['value']), user=self.render_user,
                                                            permission=AccessControlPermission.READ)
            except AccessDeniedError as err:
                return err.message
            except ObjectManagerGetError:
                return TypeReference.to_json(reference)

            try:
                ref_type = self.object_manager.get_type(ref_object.get_type_id())

                _summary_fields = []
                _nested_summaries = self.type_instance.get_nested_summaries()
                _nested_summary_fields = ref_type.get_nested_summary_fields(_nested_summaries)
                _nested_summary_line = ref_type.get_nested_summary_line(_nested_summaries)

                reference.type_id = ref_type.get_public_id()
                reference.label = ref_type.label
                reference.icon = ref_type.get_icon()
                reference.prefix = ref_type.has_nested_prefix(_nested_summaries)

                _summary_fields = _nested_summary_fields \
                    if (_nested_summary_line or _nested_summary_fields) else ref_type.get_summary().fields

                summaries = []
                summary_values = []
                for field in _summary_fields:
                    summary_value = str([x for x in ref_object.fields if x['name'] == field['name']][0]['value'])
                    summaries.append({"value": summary_value, "type": field.get('type')})
                    summary_values.append(summary_value)
                reference.summaries = summaries

                try:
                    # fill the summary line with summaries value data
                    reference.line = _nested_summary_line
                    if not reference.line_requires_fields():
                        reference.summaries = []
                    if _nested_summary_line:
                        reference.fill_line(summary_values)
                except (TypeReferenceLineFillError, Exception):
                    pass

            except ObjectManagerGetError:
                return TypeReference.to_json(reference)

        return TypeReference.to_json(reference)

    def __set_summaries(self, render_result: RenderResult) -> RenderResult:
        # global summary list
        summary_list = []
        summary_line = ''
        default_line = f'{self.type_instance.label} #{self.object_instance.public_id}'
        if not self.type_instance.has_summaries():
            render_result.summaries = summary_list
            render_result.summary_line = default_line
            return render_result
        try:
            summary_list = self.type_instance.get_summary().fields
            render_result.summaries = summary_list
            first = True

            for line in summary_list:
                if first:
                    summary_line += f'{line["value"]}'
                    first = False
                else:
                    summary_line += f' | {line["value"]}'

            render_result.summary_line = summary_line
        except Exception:
            summary_line = default_line
        finally:
            render_result.summary_line = summary_line
        return render_result

    def __set_external(self, render_result: RenderResult) -> RenderResult:
        """
        get filled external links
        Returns:
            list of filled external links (TypeExternalLink)
        """
        # global external list
        external_list = []
        # checks if type has externals defined
        if not self.type_instance.has_externals():
            render_result.externals = []
        # loop over all externals
        for ext_link in self.type_instance.get_externals():
            # append all values for required field in this list
            field_list = []
            # if data are missing or empty append here
            missing_list = []
            try:
                # get TypeExternalLink definitions from type
                ext_link_instance = self.type_instance.get_external(ext_link.name)
                # check if link requires data - regex check for {}
                if ext_link_instance.link_requires_fields():
                    # check if has fields
                    if not ext_link_instance.has_fields():
                        raise ValueError(field_list)
                    # for every field get the value data from object_instance
                    for ext_link_field in ext_link_instance.fields:
                        try:
                            if ext_link_field == 'object_id':
                                field_value = self.object_instance.public_id
                            else:
                                field_value = self.object_instance.get_value(ext_link_field)
                            if field_value is None or field_value == '':
                                # if value is empty or does not exists
                                raise ValueError(ext_link_field)
                            field_list.append(field_value)
                        except CMDBError:
                            # if error append missing data
                            missing_list.append(ext_link_instance)
                if len(missing_list) > 0:
                    raise RuntimeError(missing_list)
                try:
                    # fill the href with field value data
                    ext_link_instance.fill_href(field_list)
                except ValueError:
                    continue
            except (CMDBError, Exception):
                continue
            external_list.append(TypeExternalLink.to_json(ext_link_instance))
            render_result.externals = external_list
        return render_result


class RenderList:

    def __init__(self, object_list: List[CmdbObject], request_user: UserModel, database_manager: DatabaseManagerMongo,
                 ref_render=False, object_manager: CmdbObjectManager = None):
        self.object_list: List[CmdbObject] = object_list
        self.request_user = request_user
        self.ref_render = ref_render
        self.object_manager = object_manager
        self.type_manager = TypeManager(database_manager=database_manager)
        self.user_manager = UserManager(database_manager=database_manager)

    @timing('RenderList')
    def render_result_list(self, raw: bool = False) -> List[Union[RenderResult, dict]]:

        preparation_objects: List[RenderResult] = []
        for passed_object in self.object_list:
            tmp_render = CmdbRender(
                type_instance=self.object_manager.get_type(passed_object.type_id),
                object_instance=passed_object,
                render_user=self.request_user,
                object_manager=self.object_manager, ref_render=self.ref_render)
            if raw:
                current_render_result = tmp_render.result().__dict__
            else:
                current_render_result = tmp_render.result()
            preparation_objects.append(current_render_result)
        return preparation_objects


class RenderError(CMDBError):
    """
    Error class raised when an error occurs during rendering.
    """

    def __init__(self, message):
        self.message = f'Error while RENDER: {message}'
        super(CMDBError, self).__init__(self.message)


class TypeInstanceError(CMDBError):
    """
    Error class raised when the passed object is not an instance of TypeModel.
    """

    def __init__(self):
        self.message = "Wrong type instance"
        super(CMDBError, self).__init__(self.message)


class ObjectInstanceError(CMDBError):
    """
    Error class raised when the passed object is not an instance of CmdbObject.
    """

    def __init__(self):
        self.message = "Wrong object instance"
        super(CMDBError, self).__init__(self.message)
