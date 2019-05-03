# Net|CMDB - OpenSource Enterprise CMDB
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

from cmdb.object_framework.cmdb_object import CmdbObject
from cmdb.object_framework.cmdb_object_type import CmdbType
import logging

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
                for cs_field in curr_sum_fields:
                    try:
                        # check data
                        field_data = self.object_instance.get_value(cs_field)
                        value_list.append(field_data)
                    except CMDBError:
                        # if error while loading continue
                        continue
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
        from cmdb.object_framework.cmdb_errors import ExternalFillError
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
        from cmdb.user_management.user_manager import get_user_manager

        render_result = RenderResult(
            object_id=self.object_instance.get_public_id(),
            author_id=self.object_instance.author_id,
            author_name=get_user_manager().get_user(self.object_instance.author_id).get_name(),
            type_id=self.type_instance.get_public_id(),
            type_name=self.type_instance.get_name()
        )
        if self.has_summaries():
            pass  # render_result.set_summaries(self.get_summaries(True))
        if self.has_externals():
            pass  # render_result.set_externals(self.get_externals(True))
        return render_result


class RenderResult:

    def __init__(self, object_id: int, author_id: int, author_name: str, type_id: int, type_name: str,
                 type_label: str = None):
        self.object_id = object_id
        self.author_id = author_id
        self.author_name = author_name
        self.type_id = type_id
        self.type_name = type_name
        self.type_label = type_label or type_name.title()
        self.summaries = None
        self.externals = None

    def set_summaries(self, summary_list: list):
        self.summaries = summary_list

    def set_externals(self, external_list: list):
        self.externals = external_list

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
