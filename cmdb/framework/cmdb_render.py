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

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

import logging
from datetime import datetime
from typing import List

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.cmdb_type import CmdbType
from cmdb.user_management.user_manager import User, UserManagement

LOGGER = logging.getLogger(__name__)


class RenderVisualization:

    def __init__(self):
        self.current_render_time = datetime.utcnow()
        self.object_information: dict = {}
        self.type_information: dict = {}
        self.render_information: dict = {}

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
        self.externals: list = []


class CmdbRender:
    AUTHOR_ANONYMOUS_NAME = 'anonymous'

    def __init__(self, object_instance: CmdbObject, type_instance: CmdbType, render_user: (int, User)):
        from cmdb.user_management.user_manager import user_manager
        self.object_instance: CmdbObject = object_instance
        self.type_instance: CmdbType = type_instance
        self.__usm: UserManagement = user_manager
        # get render user if only the user id was passed
        if isinstance(render_user, int):
            self.render_user: User = self.__usm.get_user(render_user)
        self.render_user: User = render_user

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
    def type_instance(self) -> CmdbType:
        """
        Object of the class CmdbType that has already been instantiated.
        The data should come from the database and already be validated.
        This already happens when the object is instantiated.
        """
        return self._type_instance

    @type_instance.setter
    def type_instance(self, type_instance: CmdbType):
        """
        Property setter for type_instance. The render only checks whether the passed object
        belongs to the correct class, not whether it is valid.
        """
        if not isinstance(type_instance, CmdbType):
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
            author_name = self.__usm.get_user(self.object_instance.author_id).get_name()
        except CMDBError as err:
            author_name = CmdbRender.AUTHOR_ANONYMOUS_NAME
            LOGGER.error(err.message)
        render_result.object_information = {
            'object_id': self.object_instance.get_public_id(),
            'creation_time': self.object_instance.creation_time,
            'author_id': self.object_instance.author_id,
            'author_name': author_name,
            'active': self.object_instance.active,
            'version': self.object_instance.version
        }
        return render_result

    def __generate_type_information(self, render_result: RenderResult) -> RenderResult:
        try:
            author_name = self.__usm.get_user(self.type_instance.author_id).get_name()
        except CMDBError as err:
            author_name = CmdbRender.AUTHOR_ANONYMOUS_NAME
            LOGGER.error(err.message)
        render_result.type_information = {
            'type_id': self.type_instance.get_public_id(),
            'type_name': self.type_instance.name,
            'type_label': self.type_instance.label,
            'creation_time': self.type_instance.creation_time,
            'author_id': self.type_instance.author_id,
            'author_name': author_name,
            'active': self.type_instance.active,
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
        for field in self.type_instance.fields:
            try:
                field['value'] = [x for x in self.object_instance.fields if x['name'] == field['name']][0]['value']
            except ValueError:
                continue
            field_map.append(field)
        return field_map

    def __set_summaries(self, render_result: RenderResult) -> RenderResult:
        # global summary list
        summary_list = []
        # check if type has summary definition
        if not self.type_instance.has_summaries():
            render_result.summaries = summary_list
            return render_result
        for summary in self.type_instance.get_summaries():
            value_list = []
            try:
                # load summary
                curr_sum = self.type_instance.get_summary(summary['name'])
                # get field data for this summary
                curr_sum_fields = curr_sum.fields
                # get label data for this summary
                curr_label_list = []
                for cs_field in curr_sum_fields:
                    try:
                        type_fields = self.type_instance.get_fields()
                        for fields in type_fields:
                            if fields.get('name') == cs_field:
                                curr_label_list.append(fields.get('label'))
                        # check data
                        try:
                            field_data = self.object_instance.get_value(cs_field)
                        except ValueError:
                            continue
                        value_list.append(field_data)
                    except CMDBError:
                        # if error while loading continue
                        continue
                curr_sum.set_labels(curr_label_list)
                curr_sum.set_values(value_list)
            except CMDBError:
                # if error with summary continue
                continue
            summary_list.append(curr_sum.__dict__)
        render_result.summaries = summary_list
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
                            _ = self.object_instance.get_value(ext_link_field)
                            if _ is None or _ == '':
                                # if value is empty or does not exists
                                raise ValueError(ext_link_field)
                            field_list.append(_)
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

    def __init__(self, object_list: List[CmdbObject], request_user: User):
        self.object_list: List[CmdbObject] = object_list
        self.request_user = request_user

    def render_result_list(self):
        from cmdb.framework.cmdb_object_manager import object_manager
        type_buffer_list = {}
        preparation_objects = []
        for passed_object in self.object_list:
            global current_type
            current_type = None
            passed_object_type_id = passed_object.get_type_id()
            if passed_object_type_id in type_buffer_list:
                current_type = type_buffer_list[passed_object_type_id]
            else:
                try:
                    current_type = object_manager.get_type(passed_object_type_id)
                    type_buffer_list.update({passed_object_type_id: current_type})
                except CMDBError:
                    continue
            tmp_render = CmdbRender(type_instance=current_type, object_instance=passed_object,
                                    render_user=self.request_user)
            preparation_objects.append(tmp_render.result())
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
    Error class raised when the passed object is not an instance of CmdbType.
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
