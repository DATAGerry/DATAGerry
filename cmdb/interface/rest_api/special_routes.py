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

import logging

from flask import request, abort, current_app

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.route_utils import make_response, login_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.utils.error import CMDBError


with current_app.app_context():
    object_manager: CmdbObjectManager = CmdbObjectManager(current_app.database_manager)

LOGGER = logging.getLogger(__name__)
special_blueprint = RootBlueprint('special_rest', __name__, url_prefix='/special')


@special_blueprint.route('intro', methods=['GET'])
@special_blueprint.route('/intro', methods=['GET'])
@login_required
def get_intro_starter():
    try:
        steps = []
        categories_total = len(object_manager.get_categories())
        types_total = object_manager.count_types()
        objects_total = object_manager.count_objects()

        if _fetch_only_active_objs():
            result = []

            cursor = object_manager.group_objects_by_value('active', {'active': {"$eq": True}})
            for document in cursor:
                result.append(document)
            objects_total = result[0]['count'] if result else 0

        steps.append({'step': 1, 'label': 'Category', 'icon': 'check-circle',
                      'link': '/framework/category/add', 'state': categories_total > 0})

        steps.append({'step': 2, 'label': 'Type', 'icon': 'check-circle',
                      'link': '/framework/type/add', 'state': types_total > 0})

        steps.append({'step': 3, 'label': 'Object', 'icon': 'check-circle',
                      'link': '/framework/object/add', 'state': objects_total > 0})

        intro_instance = {
            'steps': steps,
            'execute': (types_total > 0 and categories_total > 0 and objects_total > 0)}

        resp = make_response(intro_instance)
    except CMDBError:
        return abort(400)
    return resp


def _fetch_only_active_objs():
    """
        Checking if request have cookie parameter for object active state
        Returns:
            True if cookie is set or value is true else false
        """
    if request.args.get('onlyActiveObjCookie') is not None:
        value = request.args.get('onlyActiveObjCookie')
        if value in ['True', 'true']:
            return True
    return False
