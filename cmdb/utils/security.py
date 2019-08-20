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

import base64
import ast
import time
import logging
from Crypto import Random
from Crypto.Cipher import AES
from cmdb.data_storage.database_manager import NoDocumentFound
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter


LOGGER = logging.getLogger(__name__)


class SecurityManager:
    DEFAULT_BLOCK_SIZE = 32
    DEFAULT_ALG = 'HS512'
    DEFAULT_EXPIRES = int(10)

    def __init__(self, database_manager, expire_time=None):
        self.ssr = SystemSettingsReader(database_manager)
        self.ssw = SystemSettingsWriter(database_manager)
        self.salt = "cmdb"
        self.expire_time = expire_time or SecurityManager.DEFAULT_EXPIRES

    def generate_hmac(self, data):
        import hashlib
        import hmac

        generated_hash = hmac.new(
            self.get_symmetric_aes_key(),
            bytes(data + self.salt, 'utf-8'),
            hashlib.sha256
        )

        generated_hash.hexdigest()

        return base64.b64encode(generated_hash.digest()).decode("utf-8")

    def encrypt_aes(self, raw):
        """
        see https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
        :param raw: unencrypted data
        :return:
        """
        if type(raw) == list:
            import json
            from bson import json_util
            raw = json.dumps(raw, default=json_util.default)
        raw = SecurityManager._pad(raw).encode('UTF-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.get_symmetric_aes_key(), AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt_aes(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.get_symmetric_aes_key(), AES.MODE_CBC, iv)
        return SecurityManager._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    @staticmethod
    def _pad(s):
        return s + (SecurityManager.DEFAULT_BLOCK_SIZE - len(s) % SecurityManager.DEFAULT_BLOCK_SIZE) * \
               chr(SecurityManager.DEFAULT_BLOCK_SIZE - len(s) % SecurityManager.DEFAULT_BLOCK_SIZE)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def generate_symmetric_aes_key(self):
        return self.ssw.write('security', {'symmetric_aes_key': Random.get_random_bytes(32)})

    def get_symmetric_aes_key(self):
        try:
            symmetric_key = self.ssr.get_value('symmetric_aes_key', 'security')
        except NoDocumentFound:
            self.generate_symmetric_aes_key()
            symmetric_key = self.ssr.get_value('symmetric_aes_key', 'security')
        return symmetric_key

    @staticmethod
    def encode_object_base_64(data: object):
        from bson.json_util import dumps
        return base64.b64encode(dumps(data).encode('utf-8')).decode("utf-8")
