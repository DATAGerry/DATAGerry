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


class CmdbLink(CmdbDAO):
    COLLECTION = "framework.links"
    REQUIRED_INIT_KEYS = [
        'primary',
        'secondary',
    ]

    def __init__(self, primary: int, secondary: int, **kwargs):
        self.primary = primary
        if primary == secondary:
            raise ValueError(f'Same link IDs: {primary}/{secondary}')
        self.secondary = secondary
        super(CmdbLink, self).__init__(**kwargs)

    def get_primary(self):
        return self.primary

    def get_secondary(self):
        return self.secondary

    def get_partners(self):
        return self.get_primary(), self.get_secondary()
