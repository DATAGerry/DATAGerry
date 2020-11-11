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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from authlib.jose import JWT
from werkzeug.wrappers import BaseResponse

from cmdb.interface.response import make_api_response
from cmdb.user_management import UserModel


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

    def make_response(self) -> BaseResponse:
        """
        Make a valid http response.

        Returns:
            Instance of BaseResponse
        """
        return make_api_response(LoginResponse.to_dict(self))

    @classmethod
    def to_dict(cls, instance: 'LoginResponse') -> dict:
        return {
            'user': UserModel.to_dict(instance.user),
            'token': instance.token.decode('UTF-8'),
            'token_issued_at': instance.token_issued_at,
            'token_expire': instance.token_expire
        }
