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
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.security.auth import AuthModule
from cmdb.security.key.holder import KeyHolder
from cmdb.security.token import DEFAULT_TOKEN_LIFETIME
from cmdb.utils.system_reader import SystemConfigReader, SystemSettingsReader

LOGGER = logging.getLogger(__name__)


class TokenGenerator:

    DEFAULT_CLAIMS = {
        'iss': {
            'essential': True,
            'value': __title__
        }
    }

    def __init__(self, database_manager: DatabaseManagerMongo = None):
        self.key_holder = KeyHolder()
        self.header = {
            'alg': 'RS512'
        }
        self.database_manager = database_manager or DatabaseManagerMongo(
            **SystemConfigReader().get_all_values_from_section('Database')
        )
        self.auth_module = AuthModule(SystemSettingsReader(self.database_manager))

    def get_expire_time(self) -> datetime:
        expire_time = int(self.auth_module.settings.get_token_lifetime(DEFAULT_TOKEN_LIFETIME))
        return datetime.now() + timedelta(minutes=expire_time)

    def generate_token(self, payload: dict, optional_claims: dict = None) -> JWT:
        optional_claims = optional_claims or {}

        token_claims = {
            'iat': int(datetime.now().timestamp()),
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
