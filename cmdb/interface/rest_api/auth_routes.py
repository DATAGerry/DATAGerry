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
import json
import logging
from datetime import datetime, timezone
from flask import request, current_app, abort

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.security.security import SecurityManager
from cmdb.manager.right_manager import RightManager
from cmdb.manager.group_manager import GroupManager
from cmdb.manager.user_manager import UserManager

from cmdb.user_management.models.user import UserModel
from cmdb.interface.route_utils import make_response, insert_request_user
from cmdb.interface.blueprint import APIBlueprint
from cmdb.security.auth import AuthModule, AuthSettingsDAO
from cmdb.security.auth.response import LoginResponse
from cmdb.security.token.generator import TokenGenerator
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.system_writer import SystemSettingsWriter
from cmdb.cmdb_objects.cmdb_section_template import CmdbSectionTemplate
from cmdb.user_management.rights import __all__ as rights
from cmdb.search import Query
from cmdb.user_management import __FIXED_GROUPS__
from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_CLASSES
from cmdb.exportd import __COLLECTIONS__ as JOB_MANAGEMENT_COLLECTION
from cmdb.manager.manager_provider import ManagerType, ManagerProvider

from cmdb.errors.provider import AuthenticationProviderNotActivated, AuthenticationProviderNotFoundError
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)

auth_blueprint = APIBlueprint('auth', __name__)

with current_app.app_context():
    dbm: DatabaseManagerMongo = current_app.database_manager

# -------------------------------------------------------------------------------------------------------------------- #

@auth_blueprint.route('/settings', methods=['GET'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_auth_settings(request_user: UserModel):
    """TODO: document"""
    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)

    auth_settings = system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__)
    auth_module = AuthModule(auth_settings)

    return make_response(auth_module.settings)


@auth_blueprint.route('/settings', methods=['POST', 'PUT'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.edit')
def update_auth_settings(request_user: UserModel):
    """TODO: document"""
    new_auth_settings_values = request.get_json()

    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)
    system_setting_writer: SystemSettingsWriter = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_WRITER,
                                                                               request_user)

    if not new_auth_settings_values:
        return abort(400, 'No new data was provided')

    try:
        new_auth_setting_instance = AuthSettingsDAO(**new_auth_settings_values)
    except Exception as err:
        return abort(400, err)

    update_result = system_setting_writer.write(_id='auth', data=new_auth_setting_instance.__dict__)

    if update_result.acknowledged:
        return make_response(system_settings_reader.get_section('auth'))

    return abort(400, 'Could not update auth settings')


@auth_blueprint.route('/providers', methods=['GET'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_installed_providers(request_user: UserModel):
    """TODO: document"""
    provider_names: list[dict] = []

    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)

    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))

    for provider in auth_module.providers:
        provider_names.append({'class_name': provider.get_name(), 'external': provider.EXTERNAL_PROVIDER})

    return make_response(provider_names)


@auth_blueprint.route('/providers/<string:provider_class>', methods=['GET'])
@insert_request_user
@auth_blueprint.protect(auth=True, right='base.system.view')
def get_provider_config(provider_class: str, request_user: UserModel):
    """TODO: document"""
    system_settings_reader: SystemSettingsReader = ManagerProvider.get_manager(ManagerType.SYSTEM_SETTINGS_READER,
                                                                               request_user)

    auth_module = AuthModule(
        system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__))

    try:
        provider_class_config = auth_module.get_provider(provider_class).get_config()
    except StopIteration:
        return abort(404, 'Provider not found')

    return make_response(provider_class_config)


@auth_blueprint.route('/login', methods=['POST'])
def post_login():
    """TODO: document"""
    user_manager: UserManager = UserManager(current_app.database_manager)
    group_manager: GroupManager = GroupManager(current_app.database_manager, right_manager=RightManager(rights))
    security_manager: SecurityManager = SecurityManager(current_app.database_manager)
    login_data = request.json

    if not request.json:
        return abort(400, 'No valid JSON data was provided')

    request_user_name = login_data['user_name']
    request_password = login_data['password']

    if current_app.cloud_mode:
        user_data = check_user_in_mysql_db(request_user_name, request_password)
        ### login data is invalid
        if not user_data:
            return abort(401, 'Could not login')

        ### no db with this name, create it
        if not check_db_exists(user_data['database']):
            init_db_routine(user_data['database'])
            create_new_admin_user(user_data)

        ### Get the user
        user = retrive_user(user_data)

        # User does not exist
        if not user:
            return abort(401, 'Could not login')

        dbm.connector.set_database(user_data['database'])

        tg = TokenGenerator(dbm)

        token: bytes = tg.generate_token(
            payload={
                'user': {
                    'public_id': user.get_public_id(),
                    'database': user.get_database()
                }
            }
        )

        token_issued_at = int(datetime.now(timezone.utc).timestamp())
        token_expire = int(tg.get_expire_time().timestamp())
        login_response = LoginResponse(user, token, token_issued_at, token_expire)

        return login_response.make_response()
    else:
        system_settings_reader: SystemSettingsReader = SystemSettingsReader(current_app.database_manager)

        auth_module = AuthModule(
            system_settings_reader.get_all_values_from_section('auth', default=AuthModule.__DEFAULT_SETTINGS__),
            user_manager=user_manager,
            group_manager=group_manager,
            security_manager=security_manager)

        user_instance = None

        try:
            user_instance = auth_module.login(request_user_name, request_password)
        except (AuthenticationProviderNotFoundError, AuthenticationProviderNotActivated):
            #TODO: ERROR-FIX
            return abort(503)
        except Exception:
            #TODO: ERROR-FIX
            return abort(401)
        finally:
            # If login success generate user instance with token
            if user_instance:
                tg = TokenGenerator(database_manager=current_app.database_manager)
                token: bytes = tg.generate_token(payload={'user': {
                    'public_id': user_instance.get_public_id()
                }})
                token_issued_at = int(datetime.now(timezone.utc).timestamp())
                token_expire = int(tg.get_expire_time().timestamp())

                login_response = LoginResponse(user_instance, token, token_issued_at, token_expire)

                return login_response.make_response()

            # Login not success
            return abort(401, 'Could not login!')


# -------------------------------------------------------------------------------------------------------------------- #
#                                                        HELPER                                                        #
# -------------------------------------------------------------------------------------------------------------------- #
def check_user_in_mysql_db(mail: str, password: str):
    """Simulates Users in MySQL DB"""

    try:
        with open('etc/test_users.json', 'r', encoding='utf-8') as users_file:
            users_data = json.load(users_file)

            if mail in users_data:
                user = users_data[mail]

                if user["password"] == password:
                    return user
            else:
                return None


    except Exception as err:
        LOGGER.debug(f"[get users from file] error: {err} , error type: {type(err)}")
        return None


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
        except Exception as error:
            LOGGER.error("Could not create admin user: %s", error)


def retrive_user(user_data: dict):
    """Get user from db"""
    dbm.connector.set_database(user_data['database'])
    loc_user_manager: UserManager = UserManager(dbm)

    try:
        return loc_user_manager.get_by(Query({'email': user_data['email']}))
    except Exception:
        return None
