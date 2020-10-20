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
from enum import Enum

from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import ApiParameters, Parameter


class GroupDeleteMode(Enum):
    NONE = None
    MOVE = 'MOVE'
    DELETE = 'DELETE'


class GroupDeletionParameters(ApiParameters):

    def __init__(self, query_string: Parameter, action: GroupDeleteMode = None, group_id: PublicID = None, **kwargs):
        """
        Constructor of the GroupDeletionParameters.

        Args:
            query_string (str): The raw http query string. Can be used when the parsed parameters are not enough.
            action (GroupDeleteMode): The action which is to perform on delete a group.
            group_id (int): The public id of another group which the users have to move.
            **kwargs: optional parameters
        """
        self.action = action
        self.group_id = group_id
        super(GroupDeletionParameters, self).__init__(query_string=query_string, **kwargs)

    @classmethod
    def from_http(cls, query_string: str, **optional) -> "GroupDeletionParameters":
        return cls(Parameter(query_string), **optional)

    @classmethod
    def to_dict(cls, parameters: "GroupDeletionParameters") -> dict:
        return {
            'action': parameters.action,
            'group_id': parameters.group_id,
            'optional': parameters.optional
        }
