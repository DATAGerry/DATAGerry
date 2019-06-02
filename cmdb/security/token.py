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

"""
Token generation module with usage of JSON Web Tokens [RFC 7519]
for more information see https://tools.ietf.org/html/rfc7519
Implementation is based on authlib https://authlib.org/
"""

import logging
import datetime
from authlib import jose

LOGGER = logging.getLogger(__name__)


class TokenGenerator:
    TIMEOUT = 120
    LEEWAY = 2
    DEFAULT_HEADER = {
        'alg': 'RS512'
    }

    DEFAULT_CLAIMS_OPTIONS = {
        'iss': {
            'essential': True,
            'value': 'cmdb'
        },
        'sub': {
            'esssential': True,
            'values': ['dict', 'user']
        }
    }

    def __init__(self, timeout: int = None):
        self.timeout = (timeout or TokenGenerator.TIMEOUT) * 60
        from cmdb.security.keys import KeyHolder
        key_holder = KeyHolder()
        self.private_key = key_holder.get_private_key()
        self.public_key = key_holder.get_public_key()

    def generate_token(self, payload: dict, sub: str = None):
        """Generate a JWT Token"""
        now = datetime.datetime.utcnow()
        payload.update({
            'iss': 'cmdb',
            'sub': sub or type(payload).__name__,
            'iat': now,
            'exp': now + datetime.timedelta(seconds=self.timeout)
        })
        return jose.jwt.encode(self.DEFAULT_HEADER, payload, self.private_key)

    def validate_token(self, token):
        """Checks if the JWT Token was signed with the private key (checks validation with public key)"""
        return jose.jwt.decode(token, self.public_key, claims_options=self.DEFAULT_CLAIMS_OPTIONS)

    def validate_token_claims(self, token):
        """Checks if the claims inside the token are valid"""
        claims = self.validate_token(token)
        return claims.validate(now=datetime.datetime.utcnow().timestamp(), leeway=self.LEEWAY)
