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
from cmdb.models.type_model.type import TypeModel
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class Update20200513(Updater):
    """TODO: document"""

    def creation_date(self):
        return '20200513'


    def description(self):
        return "Adds the property 'global_template_ids' and 'selectable_as_parent' to all types"


    def start_update(self):
        """TODO: document"""
        collection = TypeModel.COLLECTION
        all_types: list[dict] = []

        all_types = self.dbm.find_all(collection)

        for cur_type in all_types:
            #Check if the type already has the 'global_template_ids' property, else create it
            cur_public_id: int = cur_type['public_id']
            global_template_ids: str = 'global_template_ids'
            selectable_as_parent: str = 'selectable_as_parent'

            if not global_template_ids in cur_type.keys():
                cur_type[global_template_ids] = []
                self.dbm.update(collection=collection,
                                criteria={'public_id':cur_public_id},
                                data=cur_type)
                LOGGER.info("Updated 'global_template_ids' for type ID: %s", cur_public_id)

            if not selectable_as_parent in cur_type.keys():
                cur_type[selectable_as_parent] = True
                self.dbm.update(collection=collection,
                                criteria={'public_id':cur_public_id},
                                data=cur_type)
                LOGGER.info("Updated 'selectable_as_parent' for type ID: %s", cur_public_id)

        super().increase_updater_version(20200513)
