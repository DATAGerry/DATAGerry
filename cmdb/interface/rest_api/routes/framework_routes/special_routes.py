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
from flask import abort

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.objects_manager import ObjectsManager
from cmdb.manager.types_manager import TypesManager
from cmdb.manager.categories_manager import CategoriesManager

from cmdb.interface.route_utils import login_required, insert_request_user
from cmdb.interface.blueprint import RootBlueprint
from cmdb.framework.datagerry_assistant.profile_assistant import ProfileAssistant
from cmdb.user_management.models.user import UserModel
from cmdb.interface.rest_api.responses import DefaultResponse

from cmdb.errors.dg_assistant.dg_assistant_errors import ProfileCreationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

special_blueprint = RootBlueprint('special_rest', __name__, url_prefix='/special')

# -------------------------------------------------------------------------------------------------------------------- #

@special_blueprint.route('intro', methods=['GET'])
@special_blueprint.route('/intro', methods=['GET'])
@insert_request_user
@login_required
def get_intro_starter(request_user: UserModel):
    """
    Creates steps for intro and checks if there are any objects, categories or types in the DB

    Returns:
        _type_: Steps and if there are any objects, types and categories in the database
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    try:
        categories_total = categories_manager.count_categories()
        types_total = types_manager.count_types()
        objects_total = objects_manager.count_objects()

        intro_instance = {'execute': (types_total > 0 or categories_total > 0 or objects_total > 0)}

        api_response = DefaultResponse(intro_instance)

        resp = api_response.make_response()
    except Exception:
        #ERROR-FIX
        return abort(400)

    return resp


@special_blueprint.route('/profiles', methods=['POST'])
@insert_request_user
@special_blueprint.parse_assistant_parameters()
@login_required
def create_initial_profiles(data: str, request_user: UserModel):
    """
    Creates all profiles selected in the assistant

    Args:
        data (str): profile string seperated by '#'

    Returns:
        _type_: list of created public_ids of types
    """
    categories_manager: CategoriesManager = ManagerProvider.get_manager(ManagerType.CATEGORIES_MANAGER, request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)
    types_manager: TypesManager = ManagerProvider.get_manager(ManagerType.TYPES_MANAGER, request_user)

    profiles = data['data'].split('#')

    categories_total = categories_manager.count_categories()
    types_total = types_manager.count_types()
    objects_total = objects_manager.count_objects()

    # Only execute if there are no categories, types and objects in the database
    if categories_total > 0 or types_total > 0 or objects_total > 0:
        return abort(400, "There exists either objects, types or categories in the DB")

    try:
        profile_assistant = ProfileAssistant()
        created_ids = profile_assistant.create_profiles(profiles)
    except ProfileCreationError as err:
        LOGGER.debug("[create_initial_profiles] ManagerInsertError: %s", err.message)
        return abort(400, "Could not create initial profiles!")

    api_response = DefaultResponse(created_ids)

    return api_response.make_response()
