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
from cmdb.utils import SystemSettingsWriter
from cmdb.utils.system_reader import SystemConfigReader


class KeyGenerator:

    def __init__(self, key_directory=None):
        from cmdb.data_storage import get_pre_init_database
        self.ssw = SystemSettingsWriter(get_pre_init_database())
        self.key_directory = key_directory or SystemConfigReader.DEFAULT_CONFIG_LOCATION + "/keys"

    def generate_rsa_keypair(self):
        from Crypto.PublicKey import RSA
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        asymmetric_key = {
            'private': private_key,
            'public': public_key
        }
        self.ssw.write('security', {'asymmetric_key': asymmetric_key})

    def generate_symmetric_aes_key(self):
        from Crypto import Random
        self.ssw.write('security', {'symmetric_aes_key': Random.get_random_bytes(32)})
