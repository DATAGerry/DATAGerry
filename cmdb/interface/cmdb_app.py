# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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

from queue import Queue
from flask import Flask

from cmdb.database.managers import DatabaseManagerMongo


class BaseCmdbApp(Flask):

    def __init__(self, import_name: str,
                 database_manager: DatabaseManagerMongo = None,
                 event_queue: Queue = None):
        self.database_manager: DatabaseManagerMongo = database_manager
        self.event_queue: Queue = event_queue
        self.temp_folder: str = '/tmp/'

        super(BaseCmdbApp, self).__init__(import_name)

    def register_multi_blueprint(self, blueprint, multi_prefix: [str], **options):
        """
        Register a blueprint with multiple urls
        Args:
            blueprint: Original blueprint
            multi_prefix: list of url prefixes
            **options: options of flask blueprint
        """
        if 'url_prefix' in options:
            raise ValueError('Url prefix is not allow if a multi prefix was set')
        for prefix in multi_prefix:
            super(BaseCmdbApp, self).register_blueprint(blueprint, url_prefix=prefix, **options)
