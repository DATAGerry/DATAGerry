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

from datetime import datetime
from cmdb.framework.cmdb_dao import CmdbDAO


class CmdbLink(CmdbDAO):
    COLLECTION = "framework.links"
    REQUIRED_INIT_KEYS = [
        'primary',
        'secondary',
    ]

    def __init__(self, primary: int, secondary: int, creation_time: datetime = None, **kwargs):
        if primary == secondary:
            raise ValueError(f'Same link IDs: {primary}/{secondary}')
        self.primary: int = primary
        self.secondary: int = secondary
        self.creation_time: datetime = creation_time or datetime.utcnow()
        super(CmdbLink, self).__init__(**kwargs)

    def get_primary(self) -> int:
        return self.primary

    def get_secondary(self) -> int:
        return self.secondary

    def get_creation_time(self) -> datetime:
        return self.creation_time

    def get_partners(self) -> (int, int):
        return self.get_primary(), self.get_secondary()
