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
from cmdb.security.auth.auth_module import AuthModule

from cmdb.security.token.validator import TokenValidator
from cmdb.security.token.generator import TokenGenerator
from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.models.user import UserModel
from cmdb.user_management.constants import __FIXED_GROUPS__, __COLLECTIONS__ as USER_MANAGEMENT_COLLECTION
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.cmdb_objects.cmdb_section_template import CmdbSectionTemplate
from cmdb.framework.constants import __COLLECTIONS__ as FRAMEWORK_CLASSES

from cmdb.errors.manager import ManagerGetError
from cmdb.errors.security import TokenValidationError
from cmdb.errors.manager.user_manager import UserManagerInsertError, UserManagerGetError
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
        #ERROR-FIX
        LOGGER.debug("[user_has_right] Error: %s", str(err))
        return abort(401)

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

        token = parse_authorization_header(request.headers['Authorization'])
        try:
            with current_app.app_context():
                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
        except TokenValidationError:
            #ERROR-FIX
            return abort(401)

        try:
            user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

            if current_app.cloud_mode:
                database = decrypted_token['DATAGERRY']['value']['user']['database']
                users_manager = UsersManager(current_app.database_manager, database)
        except ValueError:
            return abort(401)
        except Exception as err:
            LOGGER.debug("[insert_request_user] Uncatched error type: %s", type(err))
            return abort(401)

        user = users_manager.get_user(user_id)
        kwargs.update({'request_user': user})

        return func(*args, **kwargs)

    return get_request_user

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

                auth_settings = SystemSettingsReader(current_app.database_manager).get_all_values_from_section(
                                                                                   'auth',
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

    # Generate predefined section templates
    current_app.database_manager.init_predefined_templates(CmdbSectionTemplate.COLLECTION)


def create_new_admin_user(user_data: dict):
    """Creates a new admin user"""
    LOGGER.debug("[create_new_admin_user] called")
    with current_app.app_context():
        current_app.database_manager.connector.set_database(user_data['database'])
        users_manager = UsersManager(current_app.database_manager)
        scm = SecurityManager(current_app.database_manager)

    try:
        admin_user_from_db = users_manager.get_user_by({'email': user_data['email']})

        if not admin_user_from_db:
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
        #ERROR-FIX
        return None
