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

from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.cmdb_type import CmdbType
import logging
from datetime import datetime

LOGGER = logging.getLogger(__name__)


class CmdbRender:
    __POSSIBLE_OUTPUT_FORMATS = [
        dict,
        str
    ]

    __slots__ = ['_type_instance', '_object_instance', 'format_', 'fields', 'matched_fields']

    def __init__(self, type_instance: CmdbType, object_instance: CmdbObject, format_: (dict, str) = dict):
        self.type_instance = type_instance
        self.object_instance = object_instance
        if format_ not in CmdbRender.__POSSIBLE_OUTPUT_FORMATS:
            raise WrongOutputFormat(format_)
        self.format_ = format_
        self.fields = None
        self.matched_fields = list()

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

    def _match_field_values(self) -> list:
        tmp = list()
        return tmp

    def set_matched_fieldset(self, matched_fields) -> list:
        tmp = list()
        for matched_field in matched_fields:
            try:
                tmp.append({
                    'name': matched_field,
                    'value': self.object_instance.get_value(matched_field)
                })
            except CMDBError:
                LOGGER.warning("Could not parse matched field {}".format(matched_field))
                continue
        self.matched_fields = tmp

    def get_summaries(self, output=False) -> list:
        """
        get filled summaries - list of summaries should be a string
        Returns:
            list of filled summaries
        """
        # global summary list
        summary_list = []
        # check if type has summary definition
        if not self.type_instance.has_summaries():
            return summary_list
        for sum in self.type_instance.get_summaries():
            value_list = []
            try:
                # load summary
                curr_sum = self.type_instance.get_summary(sum['name'])
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
            if output:
                summary_list.append(curr_sum.__dict__)
            else:
                summary_list.append(curr_sum)
        return summary_list

    def has_summaries(self) -> bool:
        if len(self.get_summaries()) > 0:
            return True
        else:
            return False

    def get_externals(self, output=False) -> list:
        """
        get filled external links
        Returns:
            list of filled external links (_ExternalLink)
        """
        from cmdb.framework.cmdb_errors import ExternalFillError
        # global external list
        external_list = []
        # checks if type has externals defined
        if not self.type_instance.has_externals():
            raise NoExternalLinksError(external_data=self.type_instance.render_meta['external'])
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
                        raise NoExternalFieldDataError(field_list)
                    # for every field get the value data from object_instance
                    for ext_link_field in ext_link_instance.fields:
                        try:
                            _ = self.object_instance.get_value(ext_link_field)
                            if _ is None or _ == '':
                                # if value is empty or does not exists
                                raise EmptyValueError(ext_link_field)
                            field_list.append(_)
                        except CMDBError:
                            # if error append missing data
                            missing_list.append(ext_link_instance)
                if len(missing_list) > 0:
                    raise NoExternalFieldDataError(missing_list)
                try:
                    # fill the href with field value data
                    ext_link_instance.fill_href(field_list)
                except ExternalFillError as e:
                    continue
            except CMDBError:
                continue
            # append field link to output list
            if output:
                external_list.append(ext_link_instance.__dict__)
            else:
                external_list.append(ext_link_instance)
        return external_list

    def has_externals(self) -> bool:
        try:
            self.get_externals()
            return True
        except CMDBError:
            return False

    def result(self):
        render_result = self.build_render_result()
        self.__add_extended_render_results(render_result)

        return render_result

    @staticmethod
    def result_loop_render(object_manager, instances: list) -> list:
        from cmdb.user_management.user_manager import UserManagement
        all_user = UserManagement.get_all_users_as_dict(object_manager)
        render_list = []

        for element in instances:
            render_result = element.build_render_result()
            element.__add_extended_render_results(render_result)

            dic = [i for i in all_user if (i['public_id'] == element.object_instance.author_id)]
            render_result.set_author_name('{} {}'.format(dic[0]['first_name'], dic[0]['last_name']))
            render_list.append(render_result)

        return render_list

    def build_render_result(self):
        return RenderResult(
            public_id=self.object_instance.get_public_id(),
            creation_time=self.object_instance.creation_time,
            last_edit_time=self.object_instance.last_edit_time,
            author_id=self.object_instance.author_id,
            author_name='',
            type_id=self.type_instance.get_public_id(),
            type_name=self.type_instance.get_name(),
            label=self.type_instance.get_label(),
            active=self.object_instance.active,
            version=self.object_instance.version
        )

    def __add_extended_render_results(self, render_result):
        if self.matched_fields:
            render_result.match_fields = self.matched_fields
        if self.object_instance and self.object_instance.fields:
            if self.type_instance.public_id == self.object_instance.type_id:
                for type_field in self.type_instance.fields:
                    for fields in self.object_instance.fields:
                        if fields.get('name') == type_field.get('name'):
                            fields['label'] = type_field.get('label')
                            fields['type'] = type_field.get('type')
                            fields['selected'] = self.add_selected_option([fields.get('value')],
                                                                          type_field.get('options'))
                            render_result.fields = self.object_instance.fields
        if self.has_summaries():
            render_result.set_summaries(self.get_summaries(True))
        if self.has_externals():
            render_result.set_externals(self.get_externals(True))

    def add_selected_option(self, keys: list, options: list):
        if keys is not None and len(keys) > 0 and options is not None and len(options) > 0:
            return [d for d in options if d['name'] in keys]
        return []


class RenderResult:

    def __init__(self, public_id: int, creation_time: datetime, last_edit_time: datetime,
                 author_id: int, author_name: str, version: str,
                 type_id: int, active: bool, type_name: str, label: str = None):
        self.public_id = public_id
        self.creation_time = creation_time
        self.last_edit_time = last_edit_time
        self.author_id = author_id
        self.author_name = author_name
        self.active = active
        self.type_id = type_id
        self.type_name = type_name
        self.version = version
        self.label = label or type_name.title()
        self.summaries = None
        self.externals = None
        self.match_fields = None
        self.fields = None

    def set_summaries(self, summary_list: list):
        self.summaries = summary_list

    def set_externals(self, external_list: list):
        self.externals = external_list

    def set_author_name(self, new_value):
        self.author_name = new_value

    def to_json(self):
        return self.__dict__


class TypeInstanceError(CMDBError):
    """
    Error class raised when the passed object is not an instance of CmdbType.
    """

    def __init__(self):
        self.message = "Wrong type instance"
        super(CMDBError, self).__init__(self.message)


class EmptyValueError(CMDBError):
    """
    Error when object instance value is empty or none
    """

    def __init__(self, field_name):
        self.message = "Field with this name {} do not exists or empty".format(field_name)
        super(CMDBError, self).__init__(self.message)


class NoExternalLinksError(CMDBError):
    """
    Error when type has no external links
    """

    def __init__(self, external_data):
        self.message = "Instance has no external links or required data are not defined. Data: {}".format(external_data)
        super(CMDBError, self).__init__(self.message)


class NoExternalFieldDataError(CMDBError):
    """
    Error when external link requires data which are not in field values
    """

    def __init__(self, field_list):
        self.message = "Instance has no external links. Missing fields: {}".format(field_list)
        super(CMDBError, self).__init__(self.message)


class ObjectInstanceError(CMDBError):
    """
    Error class raised when the passed object is not an instance of CmdbObject.
    """

    def __init__(self):
        self.message = "Wrong object instance"
        super(CMDBError, self).__init__(self.message)


class WrongOutputFormat(CMDBError):
    """
    Error class raised when a not support output format was chosen.
    """

    def __init__(self, output_format):
        self.message = "{} with type {} is not a supported output format".format(output_format, type(output_format))
        super(CMDBError, self).__init__(self.message)
