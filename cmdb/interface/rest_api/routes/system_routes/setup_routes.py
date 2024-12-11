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
"""
These routes are used to setup databases and the correspondig user in DATAGerry
"""
import json
import logging
from flask import request, abort, current_app

from cmdb.manager.users_manager import UsersManager

from cmdb.models.user_model.user import UserModel
from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.responses import DefaultResponse
from cmdb.interface.blueprints import APIBlueprint
from cmdb.interface.route_utils import (
    check_db_exists,
    init_db_routine,
    create_new_admin_user,
    delete_database,
    insert_api_user,
    validate_api_access,
)

from cmdb.errors.database.database_errors import DatabaseNotExists
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

setup_blueprint = APIBlueprint('setup', __name__)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@setup_blueprint.route('/subscriptions', methods=['POST'])
@insert_api_user
def create_subscription(api_user_data: dict):
    """
    Creates a database and the given user

    Hint:
    Expects a dict with the following keys:
    {
        "user_name"(str): Name of user,
        "password"(str): Password of user,
        "email"(str): Valid email of user,
        "database"(str): Name of database,
        "api_level"(int): 0 or 1 or 2,
        "config_items_limit"(int): Max number of CIs for user
    }
    """
    if not request.args:
        return abort(400, 'No request arguments provided!')

    if not validate_api_access(api_user_data, ApiLevel.SUPER_ADMIN):
        return abort(403, "No permission for this action!")

    setup_data: dict = request.args.to_dict()

    # Confirm the data is complete
    try:
        user_name = setup_data['user_name']
        password = setup_data['password']
        email = setup_data['email']
        database = setup_data['database']
        api_level = int(setup_data['api_level'])
        config_items_limit = int(setup_data['config_items_limit'])
    except KeyError:
        return abort(400, "A required field in data is missing!")

    ### Early out if databse already exists
    if check_db_exists(database):
        return abort(400, f"The database with the name {database} already exists!")

    # Create database and a new admin user
    init_db_routine(database)
    create_new_admin_user(setup_data)

    # Add the user to the users file
    try:
        with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
            users_data = json.load(users_file)

            if email in users_data:
                return abort(400, "A user with this email already exists!")

        # Create the user in the dict
        users_data[email] = {
            "user_name": user_name,
            "password": password,
            "email": email,
            "database": database,
            "active": True,
            "api_level": api_level,
            "config_items_limit": config_items_limit
        }

        with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
            json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)
    except Exception as err:
        LOGGER.debug("[create_subscription] Error: %s, Type: %s", err, type(err))
        return abort(400, "There is an issue with the users json file!")

    api_response = DefaultResponse(True)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@setup_blueprint.route('/subscriptions', methods=['GET'])
@insert_api_user
def get_all_subscriptions(api_user_data: dict):
    """
    Retrieves all subscriptions
    """
    if not validate_api_access(api_user_data, ApiLevel.SUPER_ADMIN):
        return abort(403, "No permission for this action!")

    try:
        with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
            users_data = json.load(users_file)
    except Exception as err:
        LOGGER.debug("[get_all_subscriptions] Error: %s, Type: %s", err, type(err))
        return abort(400, "There is an issue with the users json file!")

    api_response = DefaultResponse(users_data)

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@setup_blueprint.route('/subscriptions', methods=['PATCH'])
@insert_api_user
def change_subscription_status(api_user_data: dict):
    """
    Changes and the subscription user

    Hint:
    Expects a dict with the following keys:
    {
        "email"(str): Valid email of user,
        "database"(str): Name of database,
        "active"(bool): True or False
    }
    """
    if not request.args:
        return abort(400, 'No request arguments provided!')

    if not validate_api_access(api_user_data, ApiLevel.SUPER_ADMIN):
        return abort(403, "No permission for this action!")

    updated_user_data: dict = request.args.to_dict()

    # Confirm the data is complete
    try:
        user_email = updated_user_data['email']
        user_database = updated_user_data['database']
        user_active = updated_user_data['active'] in ['True', 'true', True]
    except KeyError:
        return abort(400, "A required field in data is missing!")

    try:
        with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
            users_data = json.load(users_file)

            if user_email not in users_data:
                return abort(400, "A user with this email does not exist!")

        user_data = users_data[user_email]

        # First update the user in the database then save it to the file
        users_manager = UsersManager(current_app.database_manager, user_database)

        target_user = users_manager.get_user_by({'email': user_email})
        target_user.active = user_active

        users_manager.update_user(target_user.get_public_id(), UserModel.to_dict(target_user))

        user_data['active'] = user_active

        with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
            json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)

        api_response = DefaultResponse(True)

        return api_response.make_response()
    except Exception as err:
        LOGGER.debug("[delete_subscription] Error: %s, Type: %s", err, type(err))
        return abort(400, "There is an issue with the users json file!")

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@setup_blueprint.route('/subscriptions', methods=['DELETE'])
@insert_api_user
def delete_subscription(api_user_data: dict):
    """
    Deletes a subscription
    """
    if not validate_api_access(api_user_data, ApiLevel.SUPER_ADMIN):
        return abort(403, "No permission for this action!")

    if not request.args:
        return abort(400, 'No request arguments provided!')

    delete_data: dict = request.args.to_dict()

    try:
        user_email = delete_data['email']
    except KeyError:
        return abort(400, "Email of the user which subscription should be deleted was not provided!")

    # Retrieve user_data
    try:
        with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
            users_data = json.load(users_file)

            if user_email not in users_data:
                return abort(400, "A user with this email does not exist!")

        user_data = users_data[user_email]
        user_db_name = user_data['database']

        #Remove database
        delete_database(user_db_name)

        #Remove user
        del users_data[user_email]

        with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
            json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)

    except DatabaseNotExists:
        return abort(400, f"The database with the name {user_db_name} does not exist!")
    except Exception as err:
        LOGGER.debug("[delete_subscription] Error: %s, Type: %s", err, type(err))
        return abort(400, "There is an issue with the users json file!")

    api_response = DefaultResponse(True)

    return api_response.make_response()
