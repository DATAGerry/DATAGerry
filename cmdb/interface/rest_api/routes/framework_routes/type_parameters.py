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
from json import loads

from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.utils.helpers import str_to_bool

# -------------------------------------------------------------------------------------------------------------------- #
#TODO: CLASS-FIX (move this to cmdb.interface.rest_api.responses.response_parameters)
class TypeIterationParameters(CollectionParameters):
    """TODO: document"""
    def __init__(self, query_string: str, active: bool = True, **kwargs):
        self.active = active
        super().__init__(query_string=query_string, **kwargs)


    @classmethod
    def from_http(cls, query_string: str, **optional) -> "TypeIterationParameters":
        if 'active' in optional:
            active = str_to_bool(optional.get('active', True))
            del optional['active']
        else:
            active = True
        if 'filter' in optional:
            optional['filter'] = loads(optional['filter'])
        if 'projection' in optional:
            optional['projection'] = loads(optional['projection'])
        return cls(query_string, active=active, **optional)


    @classmethod
    def to_dict(cls, parameters: "TypeIterationParameters") -> dict:
        return {**CollectionParameters.to_dict(parameters), **{'active': parameters.active}}
