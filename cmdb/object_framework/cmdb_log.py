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

from datetime import datetime
from enum import Enum

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception
from cmdb.object_framework.cmdb_dao import CmdbDAO


class LogCommands(Enum):
    CREATE = 1
    EDIT = 2
    ACTIVE = 3
    DEACTIVATE = 4


class LogModels(Enum):
    OBJECT = 'Cmd'

class CmdbLog(CmdbDAO):
    """
    State control of objects and types.
    """

    COLLECTION = "objects.logs"
    REQUIRED_INIT_KEYS = [
        'model',
        'user_id',
        'time',
        'meta',
        'state'
    ]

    def __init__(self, model: str, user_id: int, time: datetime, meta: dict = {}, state: bytearray = None, **kwargs):
        self.model = model
        self.user_id = user_id
        self.time = time
        self.meta = meta
        self.state = state
        super(CmdbLog, self).__init__(**kwargs)
