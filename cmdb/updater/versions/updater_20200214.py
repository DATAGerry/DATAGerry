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
import sys
import time
import logging
from datetime import datetime

from cmdb.updater.updater import Updater
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerUpdateError, CMDBError
from cmdb.framework.managers.object_manager import ObjectManager
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)


class Update20200214(Updater):
    """TODO: document"""


    def creation_date(self):
        return '20200214'


    def description(self):
        return 'Update the fieldtype date of CMDB objects: From string to date.'


    def start_update(self):
        """TODO: document"""
        types = self.get_types_by_field_date()
        lenx = len(types)
        for i, curr_type in enumerate(types):
            # Update objects fields
            self.worker(curr_type)
            time.sleep(0.1)
            progress = float(i) / float(lenx-1)
            if progress >= 1.:
                progress = 1

            sys.stdout.write('\b' * ((lenx+33) - i) + '')
            if i < (lenx+8):
                sys.stdout.write('')
            sys.stdout.write('\tRun: ' + str(round(progress * 100, 0)) + '%' + ' ' * ((lenx+7) - i))
            sys.stdout.flush()
        sys.stdout.write('\b\b\b\bDone!\n\n')
        self.increase_updater_version(20200214)



    def worker(self, type_):
        """TODO: document"""
        try:
            manager = ObjectManager(database_manager=self.database_manager)  # TODO: Replace when object api is updated
            object_list = self.object_manager.get_objects_by_type(type_.public_id)
            matches = type_.matches

            for obj in object_list:
                for field in obj.fields:
                    if [x for x in matches if x['name'] == field['name']]:
                        value = field['value']
                        if value:
                            if isinstance(value, datetime):
                                field['value'] = value
                            else:
                                field['value'] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                manager.update(public_id=obj.public_id, data=obj, user=None, permission=None)
        except (ObjectManagerGetError, ObjectManagerUpdateError, CMDBError) as err:
            LOGGER.error(err.message)


    def get_types_by_field_date(self):
        """TODO: document"""
        argument = []
        argument.append({'$match': {'fields.type': {'$regex': 'date'}}})
        argument.append({"$addFields": {
            "matches": {
                "$filter": {
                    "input": "$fields",
                    "as": "fields",
                    "cond": {"$eq": ["$$fields.type", 'date']}
                }
            }
        }})

        try:
            return self.object_manager.get_type_aggregate(argument)
        except ObjectManagerGetError as err:
            LOGGER.error(err.message)
            return []
