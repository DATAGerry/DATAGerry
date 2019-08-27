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
from cmdb.utils.error import CMDBError
from cmdb.utils.system_reader import SystemConfigReader, SystemSettingsReader


class KeyHolder:

    def __init__(self, key_directory=None):
        """
        Args:
            key_directory: key based directory
        """
        from cmdb.data_storage import get_pre_init_database
        self.ssr = SystemSettingsReader(get_pre_init_database())
        self.rsa_public = self.get_public_key()
        self.rsa_private = self.get_private_key()

    def get_public_key(self):
        return self.ssr.get_value('asymmetric_key', 'security')['public']

    def get_private_key(self):
        return self.ssr.get_value('asymmetric_key', 'security')['private']


class RSAKeyNotExists(CMDBError):

    def __init__(self):
        self.message = 'RSA key-pair not exists'
        super.__init__()
