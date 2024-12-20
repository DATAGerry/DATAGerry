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
import base64
import functools
import json
import logging
from datetime import datetime, timezone
from functools import wraps
from flask import request, abort, current_app
from werkzeug._internal import _wsgi_decoding_dance

from cmdb.manager.users_manager import UsersManager
from cmdb.manager.groups_manager import GroupsManager
from cmdb.manager.security_manager import SecurityManager
from cmdb.manager.settings_reader_manager import SettingsReaderManager

from cmdb.interface.rest_api.api_level_enum import ApiLevel
from cmdb.interface.rest_api.auth_method_enum import AuthMethod
from cmdb.security.auth.auth_module import AuthModule
from cmdb.security.token.validator import TokenValidator
from cmdb.security.token.generator import TokenGenerator
from cmdb.models.group_model.group import UserGroupModel
from cmdb.models.location_model.cmdb_location import CmdbLocation
from cmdb.models.user_model.user import UserModel
from cmdb.models.section_template_model.cmdb_section_template import CmdbSectionTemplate
from cmdb.models.reports_model.cmdb_report_category import CmdbReportCategory
from cmdb.models.user_management_constants import (
    __FIXED_GROUPS__,
    __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION,
)
from cmdb.framework.constants import __COLLECTIONS__ as FRAMEWORK_CLASSES

from cmdb.errors.manager import ManagerGetError
from cmdb.errors.security import TokenValidationError
from cmdb.errors.manager.user_manager import UserManagerInsertError, UserManagerGetError
from cmdb.errors.database import SetDatabaseError
from cmdb.errors.database.database_errors import DatabaseNotExists
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

DEFAULT_MIME_TYPE = 'application/json'

# -------------------------------------------------------------------------------------------------------------------- #

#@deprecated
def login_required(f):
    """
    Wraps function for routes which requires an authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """checks if user is logged in and valid
        """
        if auth_is_valid():
            return f(*args, **kwargs)

        return abort(401)

    return decorated


#@deprecated
def auth_is_valid() -> bool:
    """TODO: document"""
    try:
        parse_authorization_header(request.headers['Authorization'])
        return True
    except Exception as err:
        LOGGER.error(err)
        return False


def user_has_right(required_right: str) -> bool:
    """Check if a user has a specific right"""
    with current_app.app_context():
        users_manager = UsersManager(current_app.database_manager)
        groups_manager = GroupsManager(current_app.database_manager)

    token = parse_authorization_header(request.headers['Authorization'])

    try:
        decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
    except TokenValidationError as err:
        LOGGER.debug("[user_has_right] Error: %s", str(err))
        return abort(401, "Invalid token!")

    try:
        user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

        if current_app.cloud_mode:
            database = decrypted_token['DATAGERRY']['value']['user']['database']
            users_manager = UsersManager(current_app.database_manager, database)
            groups_manager = GroupsManager(current_app.database_manager)

        user = users_manager.get_user(user_id)
        group = groups_manager.get_group(user.group_id)
        right_status = group.has_right(required_right)

        if not right_status:
            right_status = group.has_extended_right(required_right)

        return right_status

    except ManagerGetError:
        return False


#@deprecated
def insert_request_user(func):
    """helper function which auto injects the user from the token request
    requires: login_required
    """

    @functools.wraps(func)
    def get_request_user(*args, **kwargs):
        with current_app.app_context():
            users_manager = UsersManager(current_app.database_manager)
        try:
            token = parse_authorization_header(request.headers['Authorization'])

            with current_app.app_context():
                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
        except TokenValidationError:
            #TODO: ERROR-FIX
            return abort(401)
        except Exception as err:
            LOGGER.debug("[insert_request_user] Token Exception: %s, Type: %s", err, type(err))
            return abort(401)

        try:
            user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

            if current_app.cloud_mode:
                database = decrypted_token['DATAGERRY']['value']['user']['database']
                users_manager = UsersManager(current_app.database_manager, database)

            user = users_manager.get_user(user_id)
            kwargs.update({'request_user': user})
        except ValueError:
            return abort(401)
        except Exception as err:
            LOGGER.debug("[insert_request_user] User Exception: %s, Type: %s", err, type(err))
            return abort(401)

        return func(*args, **kwargs)

    return get_request_user


def verify_api_access(*, required_api_level: ApiLevel = None):
    """TODO: document"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """TODO: document"""
            if not current_app.cloud_mode:
                return func(*args, **kwargs)

            try:
                auth_method = __get_request_auth_method()
                api_user_dict = __get_request_api_user()

                if auth_method == AuthMethod.BASIC:
                    if not __validate_api_access(api_user_dict, required_api_level):
                        return abort(403, "No permission for this action!")
            except Exception as err:
                LOGGER.warning("[verify_api_access] Exception: %s", err)
                return abort(400, "Invalid request!")

            return func(*args, **kwargs)
        return wrapper

    return decorator


def __get_request_api_user():
    """TODO: document"""
    try:
        value = _wsgi_decoding_dance(request.headers['Authorization'])

        try:
            auth_type, auth_info = value.split(None, 1)
            auth_type = auth_type.lower()
        except ValueError:
            auth_type = b"bearer"
            auth_info = value

        if auth_type in (b"basic","basic"):
            email, password = base64.b64decode(auth_info).split(b":", 1)

            with current_app.app_context():
                email = email.decode("utf-8")
                password = password.decode("utf-8")

                return {'email': email, 'password': password}
        else:
            return None
    except Exception as err:
        LOGGER.debug("[__get_request_api_user] User Exception: %s, Type: %s", err, type(err))
        return None


def __get_request_auth_method():
    """TODO: document"""
    try:
        auth_header = request.headers.get('Authorization')
        # LOGGER.debug(f"auth_header: {auth_header}")
        # LOGGER.debug(f"request: {request.method}")
        if auth_header:
            if auth_header.startswith('Basic '):
                return AuthMethod.BASIC

            if auth_header.startswith('Bearer '):
                return AuthMethod.JWT

        return abort(400, "Invalid auth method!")
    except Exception as err:
        LOGGER.debug("[insert_auth_method] User Exception: %s, Type: %s", err, type(err))
        return abort(400, "Invalid auth method!")


def __validate_api_access(user_data: dict = None, required_api_level: ApiLevel = ApiLevel.NO_API) -> bool:
    """TODO: document"""
    # Only validate in cloud mode
    if not current_app.cloud_mode:
        return True

    if not user_data or required_api_level == ApiLevel.LOCKED:
        return False

    try:
        user_instance = check_user_in_mysql_db(user_data['email'], user_data['password'])

        if user_instance:
            return user_instance['api_level'] >= required_api_level

        return False
    except Exception as err:
        LOGGER.debug("[validate_api_access] Error: %s, Type: %s", err, type(err))
        return False


# def insert_auth_method(func):
#     """TODO: document"""

#     @functools.wraps(func)
#     def get_auth_method(*args, **kwargs):
#         """TODO: document"""
#         try:
#             auth_header = request.headers.get('Authorization')

#             if auth_header:
#                 if auth_header.startswith('Basic '):
#                     kwargs.update({'auth_method': AuthMethod.BASIC})
#                 elif auth_header.startswith('Bearer '):
#                     kwargs.update({'auth_method': AuthMethod.JWT})
#                 else:
#                     return abort(400, "Invalid auth method!")
#             else:
#                 return abort(400, "Invalid auth method!")

#         except Exception as err:
#             LOGGER.debug("[insert_auth_method] User Exception: %s, Type: %s", err, type(err))
#             return abort(400, "Invalid auth method!")

#         return func(*args, **kwargs)

#     return get_auth_method


# def insert_api_user(func):
#     """TODO: document"""

#     @functools.wraps(func)
#     def get_api_user(*args, **kwargs):
#         """TODO: document"""
#         try:
#             value = _wsgi_decoding_dance(request.headers['Authorization'])

#             try:
#                 auth_type, auth_info = value.split(None, 1)
#                 auth_type = auth_type.lower()
#             except ValueError:
#                 auth_type = b"bearer"
#                 auth_info = value

#             if auth_type in (b"basic","basic"):
#                 email, password = base64.b64decode(auth_info).split(b":", 1)

#                 with current_app.app_context():
#                     email = email.decode("utf-8")
#                     password = password.decode("utf-8")

#                     kwargs.update({'api_user_data': {'email': email,
#                                                      'password': password,
#                                                      'method': "basic"}})
#             else:
#                 kwargs.update({'api_user_data': None})
#         except Exception as err:
#             LOGGER.debug("[insert_api_user] User Exception: %s, Type: %s", err, type(err))
#             kwargs.update({'api_user_data': None})

#         return func(*args, **kwargs)

#     return get_api_user


#@deprecated
def right_required(required_right: str):
    """wraps function for routes which requires a special user right
    requires: insert_request_user
    """
    def _page_right(func):
        @functools.wraps(func)
        def _decorate(*args, **kwargs):
            groups_manager = GroupsManager(current_app.database_manager)

            try:
                current_user: UserModel = kwargs['request_user']
            except KeyError:
                return abort(400, 'No request user was provided')
            try:
                if current_app.cloud_mode:
                    groups_manager = GroupsManager(current_app.database_manager, current_user.database)

                group: UserGroupModel = groups_manager.get_group(current_user.group_id)
                has_right = group.has_right(required_right)
            except ManagerGetError:
                return abort(404, 'Group or right does not exist!')

            if not has_right and not group.has_extended_right(required_right):
                return abort(403, 'Request user does not have the right for this action')

            return func(*args, **kwargs)

        return _decorate

    return _page_right


def parse_authorization_header(header):
    """
    Parses the HTTP Auth Header to a JWT Token
    Args:
        header: Authorization header of the HTTP Request
    Examples:
        request.headers['Authorization'] or something same
    Returns:
        Valid JWT token
    """
    if not header:
        return None

    value = _wsgi_decoding_dance(header)

    try:
        auth_type, auth_info = value.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        # Fallback for old versions
        auth_type = b"bearer"
        auth_info = value

    if auth_type in (b"basic","basic"):
        try:
            username, password = base64.b64decode(auth_info).split(b":", 1)

            with current_app.app_context():
                username = username.decode("utf-8")
                password = password.decode("utf-8")

                if current_app.cloud_mode:
                    user_data = check_user_in_mysql_db(username, password)

                    if not user_data:
                        return None

                    current_app.database_manager.connector.set_database(user_data['database'])

                users_manager = UsersManager(current_app.database_manager)
                security_manager = SecurityManager(current_app.database_manager)
                settings_reader = SettingsReaderManager(current_app.database_manager)

                auth_settings = settings_reader.get_all_values_from_section('auth',
                                                                            AuthModule.__DEFAULT_SETTINGS__)
                auth_module = AuthModule(auth_settings,
                                         security_manager=security_manager,
                                         users_manager=users_manager)

                try:
                    user_instance = auth_module.login(username, password)
                except Exception:
                    return None

                if user_instance:
                    tg = TokenGenerator(current_app.database_manager)

                    if current_app.cloud_mode:
                        return tg.generate_token(payload={
                                                    'user': {
                                                        'public_id': user_instance.get_public_id(),
                                                        'database': user_instance.database
                                                    }
                                                })

                    return tg.generate_token(payload={
                                                'user': {
                                                    'public_id': user_instance.get_public_id()
                                                }
                                            })

                return None
        except SetDatabaseError:
            return None
        except Exception:
            return None

    if auth_type in ("bearer", b"bearer"):
        try:
            with current_app.app_context():
                tv = TokenValidator(current_app.database_manager)
                decoded_token = tv.decode_token(auth_info)
                tv.validate_token(decoded_token)

            return auth_info
        except Exception:
            return None

    return None

# ------------------------------------------------------ HELPER ------------------------------------------------------ #

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

        return None
    except Exception as err:
        LOGGER.debug("[get users from file] Exception: %s, Type: %s", err, type(err))
        return None


def check_db_exists(db_name: dict):
    """Checks if the database exists"""
    return current_app.database_manager.check_database_exists(db_name)


def init_db_routine(db_name: str):
    """Creates a database with the given name and all corresponding collections

    Args:
        db_name (str): Name of the database
    """
    new_db = current_app.database_manager.create_database(db_name)
    current_app.database_manager.connector.set_database(new_db.name)

    with current_app.app_context():
        groups_manager = GroupsManager(current_app.database_manager)

    # Generate framework collections
    for collection in FRAMEWORK_CLASSES:
        current_app.database_manager.create_collection(collection.COLLECTION)
        # set unique indexes
        current_app.database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate user management collections
    for collection in USER_MANAGEMENT_COLLECTION:
        current_app.database_manager.create_collection(collection.COLLECTION)
        # set unique indexes
        current_app.database_manager.create_indexes(collection.COLLECTION, collection.get_index_keys())

    # Generate groups
    for group in __FIXED_GROUPS__:
        groups_manager.insert_group(group)

    # Generate the root location
    current_app.database_manager.set_root_location(CmdbLocation.COLLECTION, create=True)
    LOGGER.info("Root Location created!")

    # Generate predefined section templates
    current_app.database_manager.init_predefined_templates(CmdbSectionTemplate.COLLECTION)

    # Generate 'General' report category
    current_app.database_manager.create_general_report_category(CmdbReportCategory.COLLECTION)


def create_new_admin_user(user_data: dict):
    """Creates a new admin user"""
    with current_app.app_context():
        current_app.database_manager.connector.set_database(user_data['database'])
        users_manager = UsersManager(current_app.database_manager)
        scm = SecurityManager(current_app.database_manager)

    try:
        admin_user_from_db = users_manager.get_user_by({'email': user_data['email']})

        if not admin_user_from_db:
            admin_user = UserModel(
                public_id = 1,
                user_name = user_data['user_name'],
                email = user_data['email'],
                database = user_data['database'],
                active = True,
                api_level = int(user_data['api_level']),
                config_items_limit = int(user_data['config_items_limit']),
                group_id = 1,
                registration_time = datetime.now(timezone.utc),
                password = scm.generate_hmac(user_data['password']),
            )

            users_manager.insert_user(admin_user)
    except UserManagerGetError as err:
        raise UserManagerGetError(str(err)) from err
    except UserManagerInsertError as err:
        raise UserManagerInsertError(str(err)) from err
    except Exception as err:
        LOGGER.debug("[create_new_admin_user] Exception: %s, Type: %s", err, type(err))
        raise UserManagerInsertError(str(err)) from err


def retrive_user(user_data: dict):
    """Get user from db"""
    with current_app.app_context():
        current_app.database_manager.connector.set_database(user_data['database'])
        users_manager = UsersManager(current_app.database_manager)

    try:
        return users_manager.get_user_by({'email': user_data['email']})
    except Exception:
        #TODO: ERROR-FIX
        return None


def delete_database(db_name: str):
    """Deletes the database"""
    try:
        with current_app.app_context():
            current_app.database_manager.connector.set_database(db_name)
            users_manager = UsersManager(current_app.database_manager)

            users_manager.dbm.drop_database(db_name)
    except Exception as err:
        LOGGER.debug("[delete_database] Exception: %s, Type:%s", err, type(err))
        raise DatabaseNotExists(db_name) from err
