# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
import logging
from Crypto import Random
from Crypto.PublicKey import RSA

from cmdb.database.mongo_database_manager import MongoDatabaseManager

from cmdb.manager.settings_writer_manager import SettingsWriterManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 KeyGenerator - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class KeyGenerator:
    """TODO: document"""
    def __init__(self, dbm: MongoDatabaseManager):
        self.settings_writer = SettingsWriterManager(dbm)


    def generate_rsa_keypair(self):
        """TODO: document"""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        asymmetric_key = {
            'private': private_key,
            'public': public_key
        }

        self.settings_writer.write('security', {'asymmetric_key': asymmetric_key})


    def generate_symmetric_aes_key(self):
        """TODO: document"""
        symmetric_aes_key = Random.get_random_bytes(32)

        self.settings_writer.write('security', {'symmetric_aes_key': symmetric_aes_key})
