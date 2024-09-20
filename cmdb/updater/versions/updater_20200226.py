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
from cmdb.framework.models.category import CategoryModel
from cmdb.framework.models.type import TypeModel
from cmdb.manager.query_builder.builder_parameters import BuilderParameters

from cmdb.errors.manager.object_manager import ObjectManagerUpdateError, ObjectManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
class Update20200226(Updater):
    """TODO: document"""


    def creation_date(self):
        return '20200226'


    def description(self):
        return 'Update all types where category ID is 0, to root category public ID.'


    def start_update(self):
        try:
            # Get root category
            build_params = BuilderParameters({'root': True})
            category = self.categories_manager.iterate(build_params)
            # Update all types where category ID is 0,
            # to root category public ID
            if len(category):
                self.database_manager.update_many(TypeModel.COLLECTION, query={'category_id': 0},
                                                  update={'category_id': category.results[0].get_public_id()})

            # Remove the property root from category collection
            self.database_manager.unset_update_many(CategoryModel.COLLECTION, {}, 'root')
        except (ObjectManagerGetError, ObjectManagerUpdateError, Exception) as err:
            raise Exception(err) from err

        self.increase_updater_version(20200226)
