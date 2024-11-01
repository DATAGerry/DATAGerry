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
"""These routes are used to setup databases and the correspondig user in DATAGerry"""
import json
import logging
from flask import request, abort

from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.route_utils import make_response,\
                                       check_db_exists,\
                                       init_db_routine,\
                                       create_new_admin_user
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

setup_blueprint = APIBlueprint('setup', __name__)

# -------------------------------------------------------------------------------------------------------------------- #

@setup_blueprint.route('/create', methods=['POST'])
def setup_datagerry():
    """
    Creates a database and the given user

    Hint:
    Expects a dict with the following keys:
    {
        "user_name": Name of user,
        "password": Password of user,
        "email": Valid email of user,
        "database": Name of database
    }
    """
    LOGGER.info("setup_datagerry() called")

    if not request.args:
        return abort(400, 'No request arguments provided!')

    setup_data: dict = request.args.to_dict()

    # Confirm the data is complete
    try:
        user_name = setup_data['user_name']
        password = setup_data['password']
        email = setup_data['email']
        database = setup_data['database']
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
            "database": database
        }

        with open('etc/test_users.json', 'w', encoding='utf-8') as cur_users_file:
            json.dump(users_data, cur_users_file, ensure_ascii=False, indent=4)
    except Exception as err:
        LOGGER.debug("[setup_datagerry] Error: %s, Type: %s", err, type(err))
        return abort(400, "There is an issue with the users json file!")

    return make_response(True)
