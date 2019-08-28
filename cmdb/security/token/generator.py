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

import logging
from datetime import datetime, timedelta

from authlib.jose import jwt, JWT

from cmdb import __title__
from cmdb.security.key.holder import KeyHolder
from cmdb.utils.system_reader import SectionError, SystemConfigReader

LOGGER = logging.getLogger(__name__)


class TokenGenerator:
    DEFAULT_EXPIRE_TIME = 60

    DEFAULT_CLAIMS = {
        'iss': {
            'essential': True,
            'value': __title__
        }
    }

    def __init__(self):
        self.token_expire = 30
        self.key_holder = KeyHolder()
        self.header = {
            'alg': 'RS512'
        }

    def get_expire_time(self) -> datetime:
        try:
            expire_time = int(SystemConfigReader().get_value('expire', 'Token'))
        except (KeyError, SectionError):
            expire_time = self.DEFAULT_EXPIRE_TIME
        return datetime.now() + timedelta(minutes=expire_time)

    def generate_token(self, payload: dict, optional_claims: dict = None) -> JWT:
        optional_claims = optional_claims or {}

        token_claims = {
            'exp': int(self.get_expire_time().timestamp())
        }
        payload_claims = {
            'DATAGERRY': {
                'essential': True,
                'value': payload
            }
        }
        claims = {**self.DEFAULT_CLAIMS, **token_claims, **payload_claims, **optional_claims}
        token = jwt.encode(self.header, claims, self.key_holder.get_private_key())

        return token
