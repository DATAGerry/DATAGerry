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
from cmdb.utils.system_reader import SystemConfigReader


class KeyGenerator:

    def __init__(self, key_directory=None):
        self.key_directory = key_directory or SystemConfigReader.DEFAULT_CONFIG_LOCATION + "/keys"

    def generate_rsa_keypair(self):
        from Crypto.PublicKey import RSA
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        from pathlib import Path
        Path(f'{self.key_directory}/').mkdir(parents=True, exist_ok=True)

        file_out = open(f'{self.key_directory}/token_private.pem', "wb")
        file_out.write(private_key)
        file_out.close()

        file_out = open(f'{self.key_directory}/token_public.pem', "wb")
        file_out.write(public_key)
        file_out.close()
