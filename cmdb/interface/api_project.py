# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
"""TODO: document"""
from typing import List, Union

from cmdb.utils.error import CMDBError
# -------------------------------------------------------------------------------------------------------------------- #

class APIProjection:
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


    @staticmethod
    def __validate_inclusion(projection: dict, match: int = 1) -> list[str]:
        """
        Validation helper function to check the projection inclusion
        
        Args:
            projection (dict): Projection parameters
            match (int): Matching value in dict or list. Must be 0 or 1.

        Returns:
            list[str]: List of all keys with the matching parameters

        Raises:
            ValueError: If match is not 0 or 1
        """
        if match not in [0, 1]:
            raise ValueError('Projection parameter must be 0 or 1.')

        return [key for key, value in projection.items() if value == match]



    @property
    def includes(self) -> List[str]:
        """Get all keys which includes (value set to 1)"""
        if not self.__includes:
            self.__includes = APIProjection.__validate_inclusion(self.projection)
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
            self.__excludes = APIProjection.__validate_inclusion(self.projection, match=0)
        return self.__excludes


    def has_excludes(self) -> bool:
        """Has excludes values"""
        if not self.__has_excludes:
            self.__has_excludes = len(self.excludes) > 0
        return self.__has_excludes


class APIProjector:
    """
    Converts the API Responses based on the ApiProjection mapping.
    """
    __slots__ = '_output', '__data', '__projection'

    def __init__(self, data: Union[dict, List[dict]], projection: APIProjection = None):
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


    @staticmethod
    def element_includes(include_key: str, element: dict) -> dict:
        """Get the dict value if an elements has the include key"""
        if '.' not in include_key:
            try:
                return {include_key: element[include_key]}
            except (KeyError, ValueError, TypeError) as err:
                raise APIProjectionInclusionError(
                    f'Projected element does not include the key: {include_key} | Error: {err}') from err

        key, rest = include_key.split('.', 1)
        if isinstance(element[key], list):
            return {key: [APIProjector.element_includes(rest, e) for e in element[key]]}

        return {key: APIProjector.element_includes(rest, element[key])}


    def __parse_element(self, data: dict) -> dict:
        """Converts a single resource based on projection."""
        element = {}
        if not isinstance(data, dict):
            raise TypeError('Project elements must be a dict!')

        if self.__projection.has_includes():
            for include in self.__projection.includes:
                try:
                    element.update(self.element_includes(include, data))
                except APIProjectionInclusionError:
                    continue
        else:
            element = data

        if self.__projection.has_excludes():
            for key, item in element.copy().items():
                if key in self.__projection.excludes:
                    del element[key]  # TODO: Implement nested (dot .) parameter for exclusion.

        return element


class APIProjectionError(CMDBError):
    """TODO: document"""
    def __init__(self, message: str = None):
        self.message = message
        super().__init__()


class APIProjectionInclusionError(APIProjectionError):
    """TODO: document"""
    def __init__(self, message: str):
        message = f'Error while inclusion projection: err {message}'
        super().__init__(message)
