# dataGerry - OpenSource Enterprise CMDB
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

from authlib.jose import jwt, JWT
from authlib.jose.errors import BadSignatureError

from cmdb.security.key.holder import KeyHolder

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class TokenValidator:

    def __init__(self):
        self.key_holder = KeyHolder()

    def validate_token(self, token: (JWT, str, dict)):
        try:
            decoded_token = jwt.decode(s=token, key=self.key_holder.get_public_key())
        except BadSignatureError as err:
            raise ValidationError(err)
        return decoded_token


class ValidationError(CMDBError):

    def __init__(self, message):
        self.message = f'Error while decode the token operation - E: ${message}'
