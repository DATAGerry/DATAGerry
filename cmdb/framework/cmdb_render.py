# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Object/Type render
"""
from typing import List

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.utils.wraps import timing

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

import logging
from datetime import datetime

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.dao.type import TypeDAO
from cmdb.framework.special.dt_html_parser import DtHtmlParser
from cmdb.user_management.user_manager import User, UserManager

LOGGER = logging.getLogger(__name__)


class RenderVisualization:

    def __init__(self):
        self.current_render_time = datetime.utcnow()
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
                 type_instance: TypeDAO,
                 render_user: User, user_list: List[User] = None,
                 object_manager: CmdbObjectManager = None, dt_render=False):
        self.object_instance: CmdbObject = object_instance
        self.type_instance: TypeDAO = type_instance
        self.user_list: List[User] = user_list
        self.render_user: User = render_user
        self.object_manager = object_manager
        self.dt_render = dt_render

    def _render_username_by_id(self, user_id: int) -> str:
        user: User = None
        try:
            user = next(_ for _ in self.user_list if _.public_id == user_id)
        except Exception:
            user = None
        if user:
            return user.get_name()
        else:
            return CmdbRender.AUTHOR_ANONYMOUS_NAME

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
    def type_instance(self) -> TypeDAO:
        """
        Object of the class TypeDAO that has already been instantiated.
        The data should come from the database and already be validated.
        This already happens when the object is instantiated.
        """
        return self._type_instance

    @type_instance.setter
    def type_instance(self, type_instance: TypeDAO):
        """
        Property setter for type_instance. The render only checks whether the passed object
        belongs to the correct class, not whether it is valid.
        """
        if not isinstance(type_instance, TypeDAO):
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
            raise RenderError(f'Error while generating a CMDBResult: {err.message}')
        return render_result

    def __generate_object_information(self, render_result: RenderResult) -> RenderResult:
        try:
            author_name = self._render_username_by_id(self.object_instance.author_id)
        except CMDBError as err:
            author_name = CmdbRender.AUTHOR_ANONYMOUS_NAME
            LOGGER.error(err.message)
        render_result.object_information = {
            'object_id': self.object_instance.get_public_id(),
            'creation_time': self.object_instance.creation_time,
            'last_edit_time': self.object_instance.last_edit_time,
            'author_id': self.object_instance.author_id,
            'author_name': author_name,
            'active': self.object_instance.active,
            'version': self.object_instance.version
        }
        return render_result

    def __generate_type_information(self, render_result: RenderResult) -> RenderResult:
        try:
            author_name = self._render_username_by_id(self.type_instance.author_id)
        except CMDBError as err:
            author_name = CmdbRender.AUTHOR_ANONYMOUS_NAME
            LOGGER.error(err.message)
        try:
            self.type_instance.render_meta['icon']
        except KeyError:
            self.type_instance.render_meta['icon'] = ''
        render_result.type_information = {
            'type_id': self.type_instance.get_public_id(),
            'type_name': self.type_instance.name,
            'type_label': self.type_instance.label,
            'creation_time': self.type_instance.creation_time,
            'author_id': self.type_instance.author_id,
            'author_name': author_name,
            'icon': self.type_instance.render_meta['icon'],
            'active': self.type_instance.active,
            'clean_db': self.type_instance.clean_db,
            'version': self.type_instance.version

        }
        return render_result

    def __set_fields(self, render_result: RenderResult) -> RenderResult:
        render_result.fields = self.__merge_fields_value()
        return render_result

    def __set_sections(self, render_result: RenderResult) -> RenderResult:
        try:
            render_result.sections = self.type_instance.render_meta['sections']
        except (IndexError, ValueError):
            render_result.sections = []
        return render_result

    def __merge_fields_value(self) -> list:
        field_map = []
        html_parser = DtHtmlParser(self.object_manager)
        for field in self.type_instance.fields:
            html_parser.current_field = field
            try:
                curr_field = [x for x in self.object_instance.fields if x['name'] == field['name']][0]
                if curr_field['name'] == field['name'] and field.get('value'):
                    field['default'] = field['value']
                field['value'] = curr_field['value']
                # handle dates that are stored as strings
                if field['type'] == 'date' and isinstance(field['value'], str) and field['value']:
                    field['value'] = datetime.strptime(field['value'], '%Y-%m-%d %H:%M:%S')
                if self.dt_render:
                    field['value'] = html_parser.field_to_html(field['type'])
            except (ValueError, IndexError) as e:
                field['value'] = None
            field_map.append(field)
        return field_map

    def __set_summaries(self, render_result: RenderResult) -> RenderResult:
        # global summary list
        summary_list = []
        summary_line = ""
        if not self.type_instance.has_summaries():
            render_result.summaries = summary_list
            render_result.summary_line = f'{self.type_instance.get_label()} #{self.object_instance.public_id}  '
            return render_result
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
        return render_result

    def __set_external(self, render_result: RenderResult) -> RenderResult:
        """
        get filled external links
        Returns:
            list of filled external links (_ExternalLink)
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
                # get _ExternalLink definitions from type
                ext_link_instance = self.type_instance.get_external(ext_link['name'])
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
            external_list.append(ext_link_instance.__dict__)
            render_result.externals = external_list
        return render_result


class RenderList:

    def __init__(self, object_list: List[CmdbObject], request_user: User, dt_render=False,
                 object_manager: CmdbObjectManager = None):
        self.object_list: List[CmdbObject] = object_list
        self.request_user = request_user
        self.dt_render = dt_render
        from cmdb.utils.system_config import SystemConfigReader
        database_manager = DatabaseManagerMongo(
            **SystemConfigReader().get_all_values_from_section('Database')
        )
        self.object_manager = object_manager or CmdbObjectManager(database_manager=database_manager)
        self.user_manager = UserManager(database_manager=database_manager)

    @timing('RenderList')
    def render_result_list(self) -> List[RenderResult]:
        complete_user_list: List[User] = self.user_manager.get_users()

        preparation_objects: List[RenderResult] = []
        for passed_object in self.object_list:
            tmp_render = CmdbRender(
                type_instance=self.object_manager.get_type(passed_object.type_id),
                object_instance=passed_object,
                render_user=self.request_user, user_list=complete_user_list,
                object_manager=self.object_manager, dt_render=self.dt_render)
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
    Error class raised when the passed object is not an instance of TypeDAO.
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
