# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: document"""
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.utils.error import CMDBError
from cmdb.utils.system_reader import SystemSettingsReader
# -------------------------------------------------------------------------------------------------------------------- #


class KeyHolder:
    """TODO: document"""

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Args:
            key_directory: key based directory
        """
        self.ssr = SystemSettingsReader(database_manager)
        self.rsa_public = self.get_public_key()
        self.rsa_private = self.get_private_key()



    def get_public_key(self):
        """TODO: document"""
        return self.ssr.get_value('asymmetric_key', 'security')['public']



    def get_private_key(self):
        """TODO: document"""
        return self.ssr.get_value('asymmetric_key', 'security')['private']



class RSAKeyNotExists(CMDBError):
    """TODO: document"""
    def __init__(self):
        self.message = 'RSA key-pair not exists'
        super().__init__()
