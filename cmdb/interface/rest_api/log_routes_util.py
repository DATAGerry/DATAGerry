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
from cmdb.framework import CmdbObjectLog
from cmdb.framework.cmdb_log import LogAction


def get_log_acl_filter_query(location, log_filter: dict):
    return [
            {
                '$lookup':
                    {
                        'from': 'framework.objects',
                        'localField': 'object_id',
                        'foreignField': 'public_id',
                        'as': 'object'
                    }
            },
            {'$lookup':
                {
                    'from': 'framework.types',
                    'localField': 'object.0.type_id',
                    'foreignField': 'public_id',
                    'as': 'type'
                }
            },
            {'$unwind': {'path': '$type'}},
            {
                '$match':
                    {'$and': [
                        {'$or': [
                            {'$or': [{'type.acl': {'$exists': False}}, {'type.acl.activated': False}]},
                            {'$and': [
                                {'type.acl.activated': True},
                                {'$and': [
                                    {location: {'$exists': True}},
                                    {location: {'$all': ['READ']}}
                                ]},
                            ]}]
                        },
                        log_filter]
                    }
            },
            {'$project': {'object': 0, 'type': 0}}
        ]