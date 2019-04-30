# Net|CMDB - OpenSource Enterprise CMDB
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

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception


class CmdbLog:
    """Definition of an object log - list of state changes. """
    POSSIBLE_COMMANDS = ('create', 'edit', 'active', 'deactivate')

    def __init__(self, author_id: int, action: str, message: str, state: str = None, date: (str, datetime) = None):
        """TODO: Security manager encrypt log"""
        self.author_id = author_id
        self.action = action
        self.message = message
        self.date = date or datetime.today()
        if state is None:
            self.state = None
        else:
            self.state = state

    def get_date(self) -> datetime:
        return self.date

    def get_action(self) -> str:
        return self.action

    def get_message(self) -> str:
        return self.message

    def get_state(self) -> str:
        return self.state

    def set_state(self, state):
        self.state = state

    def __repr__(self):
        from cmdb.utils.helpers import debug_print
        return debug_print(self)


class ActionNotPossibleError(CMDBError):

    def __init__(self, action):
        super().__init__()
        self.message = 'Object log could not be set - wrong action {}'.format(action)
