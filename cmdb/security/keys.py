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
"""
Keys
"""

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

from cmdb.utils.system_reader import SystemConfigReader
from authlib.jose import JWK
from authlib.jose import JWK_ALGORITHMS


class KeyHolder:

    def __init__(self, key_directory=None):
        self.key_directory = key_directory or SystemConfigReader.DEFAULT_CONFIG_LOCATION + "/keys"
        self.rsa_public = self._load_rsa_public_key()
        self.rsa_private = self._load_rsa_private_key()

    def get_public_key(self):
        return self.rsa_public

    def get_private_key(self):
        return self.rsa_private

    def _load_rsa_public_key(self):
        rsa_p_jwk = JWK(algorithms=JWK_ALGORITHMS)
        try:
            public_pem_render = open(f'{self.key_directory}/token_public.pem', "r")
        except (FileNotFoundError, FileExistsError):
            raise RSATokenKeysNotExists()

        public_pem = public_pem_render.read()
        public_pem_render.close()
        public_pem = rsa_p_jwk.dumps(public_pem, kty='RSA')
        return public_pem

    def _load_rsa_private_key(self):
        rsa_p_jwk = JWK(algorithms=JWK_ALGORITHMS)
        try:
            public_pem_render = open(f'{self.key_directory}/token_private.pem', "r")
        except (FileNotFoundError, FileExistsError):
            raise RSATokenKeysNotExists()

        public_pem = public_pem_render.read()
        public_pem_render.close()
        public_pem = rsa_p_jwk.dumps(public_pem, kty='RSA')
        return public_pem


def _generate_rsa_keypair():
    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    from pathlib import Path
    Path(f'{SystemConfigReader.DEFAULT_CONFIG_LOCATION}keys/').mkdir(parents=True, exist_ok=True)

    file_out = open(SystemConfigReader.DEFAULT_CONFIG_LOCATION + "/keys/token_private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    file_out = open(SystemConfigReader.DEFAULT_CONFIG_LOCATION + "/keys/token_public.pem", "wb")
    file_out.write(public_key)
    file_out.close()


class RSATokenKeysNotExists(CMDBError):

    def __init__(self):
        self.message = 'RSA key-pair not exists'
        super.__init__(CMDBError, self)
