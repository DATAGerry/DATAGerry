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


import logging
from cmdb.updater.updater import Updater
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerUpdateError, CMDBError
from cmdb.framework.models.category import CategoryModel

LOGGER = logging.getLogger(__name__)


class Update20200226(Updater):

    def author(self):
        return 'sdu'

    def creation_date(self):
        return '20200226'

    def description(self):
        return 'Update the fieldtype date of CMDB objects: From string to date.'

    def increase_updater_version(self, value):
        super(Update20200226, self).increase_updater_version(value)

    def start_update(self):
        try:
            # Get root category
            root_category = self.object_manager.get_categories_by(**{'root': True})
            # Update all types where category ID is 0,
            # to root category public ID
            if len(root_category):
                self.object_manager.update_many_types(filter={'category_id': 0},
                                                      update={'$set': {'category_id': root_category[0].get_public_id()}})

            # Remove the property root from category collection
            self.object_manager.unset_update(CategoryModel.COLLECTION, 'root')
        except (ObjectManagerGetError, ObjectManagerUpdateError, CMDBError) as err:
            raise Exception(err.message)
        self.increase_updater_version(20200226)
