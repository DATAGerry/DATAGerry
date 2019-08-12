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

from cmdb.framework.cmdb_dao import CmdbDAO


class CmdbObjectLink(CmdbDAO):
    COLLECTION = "objects.links"
    REQUIRED_INIT_KEYS = [
        'partner_1',
        'partner_2',
    ]

    def __init__(self, partner_1: int, partner_2: int, **kwargs):
        self.partner_1 = partner_1
        self.partner_2 = partner_2
        super(CmdbObjectLink, self).__init__(**kwargs)

    def get_partner_1(self):
        return self.partner_1

    def get_partner_2(self):
        return self.partner_2

    def get_partners(self):
        return self.get_partner_1(), self.get_partner_2()
