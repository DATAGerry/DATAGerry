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
from typing import List, Union

from cmdb.utils.error import CMDBError


class ApiProjection:
    """
    ApiProjection is a wrapper for the api http parameters under `projection`.
    """
    __slots__ = 'projection', '__includes', '__has_includes', '__excludes', '__has_excludes'

    def __init__(self, projection: Union[dict, list] = None):
        if isinstance(projection, (list, List)):
            projection = dict.fromkeys(projection, 1)
        self.projection = projection or {}
        self.__includes = None
        self.__has_includes = None
        self.__excludes = None
        self.__has_excludes = None

    @property
    def includes(self) -> List[str]:
        """Get all keys which includes (value set to 1)"""
        if not self.__includes:
            self.__includes = [key for key, value in self.projection.items() if value == 1]
        return self.__includes

    def has_includes(self) -> bool:
        """Has include values"""
        if not self.__has_includes:
            self.__has_includes = len(self.includes) > 0
        return self.__has_includes

    @property
    def excludes(self) -> List[str]:
        """Get all keys which excludes (value set to 0)"""
        if not self.__excludes:
            self.__excludes = [key for key, value in self.projection.items() if value == 0]
        return self.__excludes

    def has_excludes(self) -> bool:
        """Has excludes values"""
        if not self.__has_excludes:
            self.__has_excludes = len(self.excludes) > 0
        return self.__has_excludes


class ApiProjector:
    """
    Converts the API Responses based on the ApiProjection mapping.
    """
    __slots__ = '_output', '__data', '__projection'

    def __init__(self, data: Union[dict, List[dict]], projection: ApiProjection = None):
        self._output = None
        self.__data = data
        self.__projection = projection

    @property
    def project(self) -> dict:
        """Outputs the projected data."""
        if not self._output:
            self._output = self.__project_output()
        return self._output

    def __project_output(self) -> Union[dict, List[dict]]:
        """Generate the output from the the api result or results"""
        if not self.__projection:
            return self.__data

        if isinstance(self.__data, list):
            output = []
            for element in self.__data:
                output.append(self.__parse_element(element))
        else:
            output = self.__parse_element(self.__data)

        return output

    def __parse_element(self, data: dict) -> dict:
        """Converts a single resource based on projection."""
        element = {}
        if not isinstance(data, dict):
            raise TypeError('Project elements must be a dict!')

        if self.__projection.has_includes():
            for key, item in data.items():
                if key in self.__projection.includes:
                    element.update({key: item})
        else:
            element = data

        if self.__projection.has_excludes():
            for key, item in element.copy().items():
                if key in self.__projection.excludes:
                    del element[key]

        return element


class ApiProjectionError(CMDBError):

    def __init__(self, message: str = None):
        self.message = message
        super(ApiProjectionError, self).__init__()
