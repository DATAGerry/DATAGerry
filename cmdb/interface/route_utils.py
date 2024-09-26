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
from functools import wraps
from datetime import datetime
from flask import request, abort, current_app, make_response as flask_response
from werkzeug._internal import _wsgi_decoding_dance

from cmdb.user_management.managers.user_manager import UserManager
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.right_manager import RightManager
from cmdb.security.security import SecurityManager
from cmdb.security.auth import AuthModule

from cmdb.security.token.generator import TokenGenerator
from cmdb.user_management import UserGroupModel
from cmdb.user_management.rights import __all__ as rights
from cmdb.user_management.models.user import UserModel
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils import json_encoding

from cmdb.security.token.validator import TokenValidator

from cmdb.errors.manager import ManagerGetError
from cmdb.errors.security import TokenValidationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

DEFAULT_MIME_TYPE = 'application/json'

# -------------------------------------------------------------------------------------------------------------------- #

def default(obj):
    """Json encoder for database values."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


#@deprecated
def make_response(instance, status_code=200, indent=2):
    """
    make json http response with indent settings and auto encoding
    Args:
        instance: instance of a cmdbDao instance or instance of the subclass
        status_code: optional status code
        indent: indent of json response
    Returns:
        http valid response
    """
    # encode the dict data from the object to json data
    resp = flask_response(json.dumps(instance, default=json_encoding.default, indent=indent), status_code)
    resp.mimetype = DEFAULT_MIME_TYPE

    return resp


#@deprecated
def login_required(f):
    """
    Wraps function for routes which requires an authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        """checks if user is logged in and valid
        """
        valid = auth_is_valid()
        if valid:
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
        user_manager = UserManager(current_app.database_manager)
        group_manager = GroupManager(current_app.database_manager, RightManager(rights))

    token = parse_authorization_header(request.headers['Authorization'])

    try:
        decrypted_token = TokenValidator(database_manager=current_app.database_manager).decode_token(token)
    except TokenValidationError as err:
        #TODO: ERROR-FIX
        LOGGER.debug("[user_has_right] Error: %s", str(err))
        return abort(401)

    try:
        user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

        if current_app.cloud_mode:
            database = decrypted_token['DATAGERRY']['value']['user']['database']
            user_manager = UserManager(current_app.database_manager, database)
            group_manager = GroupManager(current_app.database_manager, RightManager(rights), database)

        user = user_manager.get(user_id)
        group = group_manager.get(user.group_id)
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
            user_manager = UserManager(current_app.database_manager)

        token = parse_authorization_header(request.headers['Authorization'])
        try:
            with current_app.app_context():
                decrypted_token = TokenValidator(current_app.database_manager).decode_token(token)
        except TokenValidationError:
            #TODO: ERROR-FIX
            return abort(401)

        try:
            user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']

            if current_app.cloud_mode:
                database = decrypted_token['DATAGERRY']['value']['user']['database']
                user_manager = UserManager(current_app.database_manager, database)
        except ValueError:
            return abort(401)
        except Exception as err:
            LOGGER.debug("[insert_request_user] Uncatched error type: %s", type(err))
            return abort(401)

        user = user_manager.get(user_id)
        kwargs.update({'request_user': user})

        return func(*args, **kwargs)

    return get_request_user


#@deprecated
def right_required(required_right: str, excepted: dict = None):
    """wraps function for routes which requires a special user right
    requires: insert_request_user
    """
    def _page_right(func):
        @functools.wraps(func)
        def _decorate(*args, **kwargs):
            group_manager = GroupManager(current_app.database_manager, RightManager(rights))

            try:
                current_user: UserModel = kwargs['request_user']
            except KeyError:
                return abort(400, 'No request user was provided')
            try:
                if current_app.cloud_mode:
                    group_manager = GroupManager(current_app.database_manager,
                                                 RightManager(rights),
                                                 current_user.database)

                group: UserGroupModel = group_manager.get(current_user.group_id)
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

                user_manager: UserManager = UserManager(current_app.database_manager)
                group_manager: GroupManager = GroupManager(current_app.database_manager, RightManager(rights))
                security_manager: SecurityManager = SecurityManager(current_app.database_manager)

                auth_settings = SystemSettingsReader(current_app.database_manager).get_all_values_from_section(
                                                                                   'auth',
                                                                                   AuthModule.__DEFAULT_SETTINGS__)
                auth_module = AuthModule(auth_settings,
                                         user_manager=user_manager,
                                         group_manager=group_manager,
                                         security_manager=security_manager)

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
                    else:
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


    except Exception as err:
        LOGGER.debug(f"[get users from file] error: {err} , error type: {type(err)}")
        return None
