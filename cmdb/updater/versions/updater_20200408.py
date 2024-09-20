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

from cmdb.updater.updater import Updater
from cmdb.framework.cmdb_object import CmdbObject

from cmdb.errors.manager.object_manager import ObjectManagerUpdateError, ObjectManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
class Update20200408(Updater):
    """TODO: document"""

    def creation_date(self):
        return '20200408'


    def description(self):
        return 'Fix possible wrong object counter'


    def start_update(self):
        try:
            collection = CmdbObject.COLLECTION
            highest_id = self.database_manager.get_highest_id(collection)
            self.database_manager.update_public_id_counter(collection, highest_id)

        except (ObjectManagerGetError, ObjectManagerUpdateError, Exception) as err:
            raise Exception(err) from err

        self.increase_updater_version(20200408)
