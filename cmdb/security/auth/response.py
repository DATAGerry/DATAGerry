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
from werkzeug.wrappers import Response

from cmdb.user_management.models.user import UserModel
from cmdb.interface.rest_api.responses.get_single_value_response import GetSingleValueResponse
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 LoginResponse - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class LoginResponse:
    """Basic login instance for returning a login data"""

    __slots__ = 'user', 'token', 'token_issued_at', 'token_expire'

    def __init__(self, user: UserModel, token: bytes, token_issued_at: int, token_expire: int):
        """
        Constructor of `LoginResponse`

        Args:
            user (UserModel): Instance of the selected user
            token (bytes): A valid JW Token
            token_issued_at: The timestamp when the token was issued.
            token_expire: The timestamp when the token expires.
        """
        self.user = user
        self.token = token
        self.token_issued_at = token_issued_at
        self.token_expire = token_expire


    def make_response(self) -> Response:
        """
        Make a valid http response.

        Returns:
            Instance of Response
        """
        return GetSingleValueResponse(LoginResponse.to_dict(self)).make_response()


    @classmethod
    def to_dict(cls, instance: 'LoginResponse') -> dict:
        """TODO: document"""
        return {
            'user': UserModel.to_dict(instance.user),
            'token': instance.token.decode('UTF-8'),
            'token_issued_at': instance.token_issued_at,
            'token_expire': instance.token_expire
        }
