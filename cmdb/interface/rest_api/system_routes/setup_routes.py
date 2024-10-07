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
from datetime import datetime, timezone

from flask import request, current_app

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.manager.group_manager import GroupManager
from cmdb.manager.user_manager import UserManager
from cmdb.security.security import SecurityManager

from cmdb.search import Query
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import ErrorMessage
from cmdb.interface.route_utils import make_response
from cmdb.cmdb_objects.cmdb_section_template import CmdbSectionTemplate
from cmdb.user_management.models.user import UserModel
from cmdb.user_management import __FIXED_GROUPS__, __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_CLASSES
from cmdb.exportd import __COLLECTIONS__ as JOB_MANAGEMENT_COLLECTION
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

setup_blueprint = APIBlueprint('setup', __name__)

with current_app.app_context():
    dbm: DatabaseManagerMongo = current_app.database_manager

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
        return ErrorMessage(400, 'No request arguments provided!').response()

    setup_data: dict = request.args.to_dict()

    # Confirm the data is complete
    try:
        user_name = setup_data['user_name']
        password = setup_data['password']
        email = setup_data['email']
        database = setup_data['database']
    except KeyError:
        return ErrorMessage(400, "A required field in data is missing!").response()

    ### Early out if databse already exists
    if check_db_exists(database):
        return ErrorMessage(400, f"The database with the name {database} already exists!").response()

    # Create database and a new admin user
    init_db_routine(database)
    create_new_admin_user(setup_data)

    # Add the user to the users file
    try:
        with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
            users_data = json.load(users_file)

            if email in users_data:
                return ErrorMessage(400, "A user with this email already exists!").response()

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
        LOGGER.debug(f"[setup_datagerry] Error: {err}, Type: {type(err)}")
        return ErrorMessage(400, "There is an issue with the users json file!").response()

    return make_response(True)

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

def check_db_exists(db_name: dict):
    """Checks if the database exists"""
    return dbm.check_database_exists(db_name)


def init_db_routine(db_name: str):
    """Creates a database with the given name and all corresponding collections

    Args:
        db_name (str): Name of the database
    """
    new_db = dbm.create_database(db_name)
    dbm.connector.set_database(new_db.name)
    group_manager = GroupManager(dbm)

    # Generate framework collections
    for collection in FRAMEWORK_CLASSES:
        dbm.create_collection(collection.COLLECTION)
        # set unique indexes
        dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate user management collections
    for collection in USER_MANAGEMENT_COLLECTION:
        dbm.create_collection(collection.COLLECTION)
        # set unique indexes
        dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate ExportdJob management collections
    for collection in JOB_MANAGEMENT_COLLECTION:
        dbm.create_collection(collection.COLLECTION)
        # set unique indexes
        dbm.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate groups
    for group in __FIXED_GROUPS__:
        group_manager.insert(group)

    # Generate predefined section templates
    dbm.init_predefined_templates(CmdbSectionTemplate.COLLECTION)


def create_new_admin_user(user_data: dict):
    """Creates a new admin user"""
    dbm.connector.set_database(user_data['database'])

    loc_user_manager: UserManager = UserManager(dbm)
    scm = SecurityManager(dbm)

    try:
        loc_user_manager.get_by(Query({'email': user_data['email']}))
    except Exception: # Admin user was not found in the database, create a new one
        admin_user = UserModel(
            public_id=1,
            user_name=user_data['user_name'],
            email=user_data['email'],
            database=user_data['database'],
            active=True,
            group_id=1,
            registration_time=datetime.now(timezone.utc),
            password=scm.generate_hmac(user_data['password']),
        )

        try:
            loc_user_manager.insert(admin_user)
        except Exception as err:
            LOGGER.error("Could not create admin user: %s", err)