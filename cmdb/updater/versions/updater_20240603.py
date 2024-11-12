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
from cmdb.models.cmdb_object import CmdbObject
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)

class Update20240603(Updater):
    """TODO: document"""

    def creation_date(self):
        return '20240603'


    def description(self):
        return """
                Add the property 'multi_data_sections' to all objects which don't have it
               """


    def start_update(self):
        """TODO: document"""
        collection = CmdbObject.COLLECTION
        all_objects: list[dict] = []

        all_objects = self.dbm.find_all(collection)

        for cur_obj in all_objects:
            # Check if the object already has the property 'multi_data_sections', else create it
            if not 'multi_data_sections' in cur_obj.keys():
                cur_public_id = cur_obj['public_id']
                cur_obj['multi_data_sections'] = []

                self.dbm.update(collection=collection,
                                criteria={'public_id':cur_public_id},
                                data=cur_obj)
                LOGGER.info("Updated 'multi_data_sections' for object ID: %s", cur_public_id)

        super().increase_updater_version(20240603)
