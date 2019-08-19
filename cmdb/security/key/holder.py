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
from cmdb.utils.error import CMDBError
from cmdb.utils.system_reader import SystemConfigReader


class KeyHolder:

    def __init__(self, key_directory=None):
        """
        Args:
            key_directory: key based directory
        """
        self.key_directory = key_directory or SystemConfigReader.DEFAULT_CONFIG_LOCATION + "/keys"
        self.rsa_public = self.get_public_pem()
        self.rsa_private = self.get_private_pem()

    def get_public_key(self):
        return self.rsa_public

    def get_private_key(self):
        return self.rsa_private

    def get_public_pem(self):
        try:
            public_pem_render = open(f'{self.key_directory}/token_public.pem', "r")
        except (FileNotFoundError, FileExistsError):
            raise RSAKeyNotExists()

        public_pem = public_pem_render.read()
        public_pem_render.close()
        return public_pem

    def get_private_pem(self):
        try:
            private_pem_reader = open(f'{self.key_directory}/token_private.pem', "r")
        except (FileNotFoundError, FileExistsError):
            raise RSAKeyNotExists()

        private_pem = private_pem_reader.read()
        private_pem_reader.close()
        return private_pem


class RSAKeyNotExists(CMDBError):

    def __init__(self):
        self.message = 'RSA key-pair not exists'
        super.__init__()
