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
from cmdb.updater.updater import Updater


class Update20201012(Updater):
    """
    Updater for user settings update.
    Insert the management.users.settings collection into the database.
    """

    def author(self):
        return 'mh'

    def creation_date(self):
        return '20201012'

    def description(self):
        return 'Add user settings collection to database'

    def increase_updater_version(self, value: int):
        super(Update20201012, self).increase_updater_version(value)

    def start_update(self):
        from cmdb.user_management.models.settings import UserSettingModel
        self.increase_updater_version(20201012)
        self.database_manager.create_collection(UserSettingModel.COLLECTION)
        self.database_manager.create_indexes(UserSettingModel.COLLECTION, UserSettingModel.get_index_keys())
