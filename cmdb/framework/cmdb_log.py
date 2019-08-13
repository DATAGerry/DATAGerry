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

import logging

from datetime import datetime
from enum import Enum

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception
from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.framework.cmdb_object import CmdbObject
from cmdb.framework.cmdb_object_type import CmdbType

LOGGER = logging.getLogger(__name__)


class LogCommands(Enum):
    CREATE = 1
    EDIT = 2
    ACTIVE = 3
    DEACTIVATE = 4


class LogModels(Enum):
    OBJECT = CmdbObject.__class__.__name__
    TYPE = CmdbType.__class__.__name__


class CmdbLog(CmdbDAO):
    """
    State control of objects and types.
    """

    COLLECTION = "framework.logs"
    REQUIRED_INIT_KEYS = [
        'model',
        'user_id',
        'time',
        'meta',
        'state'
    ]

    def __init__(self, model: str, action: LogCommands, user_id: int, time: datetime, meta: dict = None,
                 state: bytearray = None, **kwargs):
        self.model = model
        self.action = action
        self.user_id = user_id
        self.time = time
        self.meta = meta or {}
        self.state = state or None
        super(CmdbLog, self).__init__(**kwargs)

    def get_decrypted_state(self) -> (LogModels.OBJECT, LogModels.TYPE):
        from cmdb.security.keys import KeyHolder
        from cmdb.security.crypto import RSADecryption
        key_holder = KeyHolder()
        rsa_dec = RSADecryption(private_key_pem=key_holder.get_private_pem())
        rsa_decrypted = rsa_dec.decrypt(self.state)
        LOGGER.debug(rsa_decrypted)
        return rsa_decrypted

    def encrypt_state(self, data: (LogModels.OBJECT, LogModels.TYPE)):
        from cmdb.security.keys import KeyHolder
        from cmdb.security.crypto import RSAEncryption
        key_holder = KeyHolder()
        rsa_enc = RSAEncryption(public_key_pem=key_holder.get_public_pem())
        LOGGER.debug(rsa_enc)
        self.state = rsa_enc.encrypt(data.to_database())
