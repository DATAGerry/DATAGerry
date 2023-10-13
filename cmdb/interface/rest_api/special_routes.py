# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
from cmdb.framework.assistant_profiles.profiles import ProfileAssistant
from cmdb.manager.errors import ManagerInsertError


with current_app.app_context():
    object_manager: CmdbObjectManager = CmdbObjectManager(current_app.database_manager)

LOGGER = logging.getLogger(__name__)
special_blueprint = RootBlueprint('special_rest', __name__, url_prefix='/special')


@special_blueprint.route('intro', methods=['GET'])
@special_blueprint.route('/intro', methods=['GET'])
@login_required
def get_intro_starter():
    """
    Creates steps for intro and checks if there are any objects, categories or types in the DB

    Returns:
        _type_: Steps and if there are any objects, types and categories in the database
    """
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


@special_blueprint.route('/profiles', methods=['POST'])
@special_blueprint.parse_assistant_parameters()
@login_required
def create_initial_profiles(data: str):
    """
    Creates all profiles selected in the assistant

    Args:
        data (str): profile string seperated by '#'

    Returns:
        _type_: list of created public_ids of types
    """
    profiles = data['data'].split('#')

    categories_total = len(object_manager.get_categories())
    types_total = object_manager.count_types()
    objects_total = object_manager.count_objects()

    # only execute if there are no categories, types and objects in the database
    if categories_total == 0 and types_total == 0 and objects_total == 0:
        LOGGER.info("EMPTY DB")
    else:
        LOGGER.info("STUFF in DB")

    try:
        profile_assistant = ProfileAssistant()
        created_ids = profile_assistant.create_profiles(profiles)
    except ManagerInsertError as err:
        return abort(400, err.message)

    return make_response(created_ids)


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
