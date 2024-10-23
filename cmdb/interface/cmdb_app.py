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

from queue import Queue
from flask import Flask

from cmdb import __CLOUD_MODE__
from cmdb.database.mongo_database_manager import MongoDatabaseManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class BaseCmdbApp(Flask):
    """TODO: document"""

    def __init__(self, import_name: str,
                 database_manager: MongoDatabaseManager = None,
                 event_queue: Queue = None):
        #REFACTOR-FIX (replace self.database_manager with self.dbm)
        self.database_manager: MongoDatabaseManager = database_manager
        self.event_queue: Queue = event_queue
        self.temp_folder: str = '/tmp/'
        self.cloud_mode = __CLOUD_MODE__

        # if self.cloud_mode:
        self.asymmetric_key = {
            'private': b'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAmFEdxz3bGXnCYuKX2AFliOytBbsTrJWI/iLqzBX1EZSL0s1c\nf+bFAez8fvpJRtlvlIpbj+a7v8REbgL6JsKVuT24SfadVb4UQOCtcPyWQSc0MPdY\nqQM+4RpKGyHqoo48+EqkiTbtBNX39Vox5TilbDKgrcbsEd+J05H4dmIdu1do1aCg\nbF/MHUo1vdgLMQXKz8aj9QAj9wy7PgpmUSQk5hT/eRl4TD+ZntnnI5L0FYU9LMS5\nlyANGETs5LpmHBK/E9kwu9+cSwKwg2UQvxEiHov1gxome03Q9JRawXiz4oeWyAVh\nn04w83C7HfUIJg3cSuuP9e95zLDqiloRmAzjuQIDAQABAoIBAA+swlohlhmDL6NW\nQw7YRvMOOziUod/QBDj2DjB6Pn4Eidaj6mXhsWrDMRFer7mOMRbJ3cYbdj0UBUBG\nh2iDfB3D+aIH8nVTUjmCfarb3ZkfIBZ9b+b1xevrtQ5hgUhhB6p8IP5bdA0cOXAr\nC+k1WQW/WIyFpP/qX6BRnG6PZpSjr5ka+o3TKHePU0LjQiI3VGj7bpuzQEmJ4OSp\nCRRzkxHWJ/4BY8Mpb2NlWmvBUKwiz0R7w31awH+mRX2m+ne12uXblgsJpcrgsS2I\n7EiXx+1oDeMKqWx/p3A1baXXH6iqAWUvA19E/NZDjxR8HuUgOaZK2phjzzJFyfGL\nxqdJxHECgYEAunYcNFil6/tAftv0nhX2fanHn/kKufD1TTF8wahtclyXELD4FKTl\nEOz4j6lx3mefF/rtFIyTpbVjGWEC6f0ZxHXloynMRht5NIjmgEJRTBmdGnn6mH7G\nxf6pKkIviXxMzUQEqBqHSiWnPNWMzGgPErXrmCbDodfwScvq9j+NFZECgYEA0R8n\nDzxPE1podpajBCKSb2hS0Bw1fKs/gFyxowcA/TGH7A1a8k0PMh/z5oGrSUGH5ny3\nmtN9yBKYrTuDXVSKyycJI/CEJLsUQBFvl6Chi4yF2pc60adnnJIuSO1LpHNPLEFK\niSjUgVy6zg3BT2FuYuzWmTlYz34/4I1T3CYPt6kCgYBcdsOHxcoJ2p9iCUsltbh1\nGmNO1h3WlUHflMHL+uzDQFz9PvTWr+qT2R9thlZcNsBzENDOVuPE0c0hwbTDOeq0\nPM6yecC9p1QUlCrRwZE1DqKUhZaaVovVlXJn7UhLgmNHiwpQHk+mmkNzbGaU2qlW\n2vXIjriGomGbBs8ua9dXsQKBgD8HnbU43zidEklUA9RWOz66+eLh7bkiwGQHDD9v\n9/tYd3hNWjEXytG30cKTKLZOuxBcXNackhfAiyYDfwedWKv8mwOrFZkgjez1lGXm\nM2qlMx78X+0bAN6vLKYsZ5UscBuNnlKS7OIEugUrHi231xaX/eJ25266xbP/xNvg\n2PHpAoGAdvSh+sk0sND4psRcP/Gpx3ey+/BD6G4XQiewtvMJMNb5T9FnYoesU70Q\nmQ7sp8eSTmvfyRNtHwUDdfCF+bycdc5aXiQSKZPlgA2sc5NyZ38g37En8PBAQqHC\nqBfGj4rTzhS75P72w3isT06TocYd+ulWZVZPAlTV6T4WyWleWf4=\n-----END RSA PRIVATE KEY-----',
            'public': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmFEdxz3bGXnCYuKX2AFl\niOytBbsTrJWI/iLqzBX1EZSL0s1cf+bFAez8fvpJRtlvlIpbj+a7v8REbgL6JsKV\nuT24SfadVb4UQOCtcPyWQSc0MPdYqQM+4RpKGyHqoo48+EqkiTbtBNX39Vox5Til\nbDKgrcbsEd+J05H4dmIdu1do1aCgbF/MHUo1vdgLMQXKz8aj9QAj9wy7PgpmUSQk\n5hT/eRl4TD+ZntnnI5L0FYU9LMS5lyANGETs5LpmHBK/E9kwu9+cSwKwg2UQvxEi\nHov1gxome03Q9JRawXiz4oeWyAVhn04w83C7HfUIJg3cSuuP9e95zLDqiloRmAzj\nuQIDAQAB\n-----END PUBLIC KEY-----'
        }

        self.symmetric_key = b'\x11\xeb\x8d*C\x95\xdd\xec0\xca7\x9ds\x92\xe9\x9b\x1e|i\x92i\x1c\x90\x8aw\xcd\x9aT\xbf\x1b)\x83'

        super().__init__(import_name)
