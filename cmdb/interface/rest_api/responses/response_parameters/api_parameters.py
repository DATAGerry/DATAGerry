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
import logging
from json import loads
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 APIParameters - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class APIParameters:
    """Rest API Parameter superclass"""

    def __init__(self, query_string: str = None, projection: dict = None, **optional):
        self.query_string: str = query_string or ''
        self.projection: dict = projection
        self.optional = optional


    @classmethod
    def from_http(cls, query_string: str, **optional) -> "APIParameters":
        """TODO: document"""
        if 'projection' in optional:
            optional['projection'] = loads(optional['projection'])
        return cls(query_string, **optional)


    @classmethod
    def to_dict(cls, parameters: "APIParameters") -> dict:
        """Get the object as a dict"""
        params: dict = {
            'query_string': parameters.query_string
        }
        if parameters.projection:
            params.update({'projection': parameters.projection})
        return params


    def __repr__(self):
        return f'Parameters: Query({self.query_string}) | Projection({self.projection}) |Optional({self.optional})'
