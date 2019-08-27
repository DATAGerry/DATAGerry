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

from cmdb.framework.cmdb_dao import CmdbDAO


class CmdbStatus(CmdbDAO):
    MAX_SHORT_LENGTH = 5
    COLLECTION = "framework.status"
    REQUIRED_INIT_KEYS = [
        'name'
    ]
    INDEX_KEYS = [
        {'keys': [('name', CmdbDAO.DAO_ASCENDING)], 'name': 'name', 'unique': True}
    ]

    def __init__(self, name: str, label: str = None, short: str = None, color: str = None, icon: str = None,
                 events: list = None, **kwargs):
        self.name = name
        self.label = label or self.name.title()
        short = short or name
        self.short = (
            (short[:CmdbStatus.MAX_SHORT_LENGTH]) if len(short) > CmdbStatus.MAX_SHORT_LENGTH else short).upper()
        self.color = color
        self.icon = icon
        self.events = events or []
        super(CmdbStatus, self).__init__(**kwargs)

    def get_name(self) -> str:
        return self.name

    def get_label(self) -> str:
        return self.label

    def get_short(self) -> str:
        return self.short

    def get_events(self) -> list:
        return self.events
