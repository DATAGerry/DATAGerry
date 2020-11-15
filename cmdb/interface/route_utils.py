# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2020 NETHINKS GmbH
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import base64
import functools
import json
import calendar
from functools import wraps
from datetime import datetime

from werkzeug._compat import to_unicode
from werkzeug.http import wsgi_to_bytes

from cmdb.manager.errors import ManagerGetError
from cmdb.security.auth import AuthModule
from cmdb.security.token.generator import TokenGenerator
from cmdb.user_management import UserGroupModel
from cmdb.user_management.rights import __all__ as rights
from cmdb.user_management.models.user import UserModel
from cmdb.user_management.managers.user_manager import UserManager
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.right_manager import RightManager
from cmdb.utils.system_reader import SystemSettingsReader
from cmdb.utils.wraps import LOGGER

from flask import request, abort, current_app

from cmdb.security.token.validator import TokenValidator, ValidationError
from cmdb.utils.wraps import deprecated
from cmdb.utils import json_encoding

DEFAULT_MIME_TYPE = 'application/json'


def default(obj):
    """Json encoder for database values."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


@deprecated
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
    from flask import make_response as flask_response

    # encode the dict data from the object to json data
    resp = flask_response(json.dumps(instance, default=json_encoding.default, indent=indent), status_code)
    # add header information
    resp.mimetype = DEFAULT_MIME_TYPE
    return resp


@deprecated
def login_required(f):
    """wraps function for routes which requires an authentication
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """checks if user is logged in and valid
        """
        valid = auth_is_valid()
        if valid:
            return f(*args, **kwargs)
        else:
            return abort(401)

    return decorated


@deprecated
def auth_is_valid() -> bool:
    try:
        parse_authorization_header(request.headers['Authorization'])
        return True
    except Exception as err:
        LOGGER.error(err)
        return False


def user_has_right(required_right: str) -> bool:
    """Check if a user has a specific right"""
    from flask import request, current_app
    with current_app.app_context():
        user_manager = UserManager(current_app.database_manager)
        group_manager = GroupManager(current_app.database_manager, RightManager(rights))

    token = parse_authorization_header(request.headers['Authorization'])
    try:
        decrypted_token = TokenValidator().decode_token(token)
    except ValidationError as err:
        return abort(401)
    try:
        user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']
        user = user_manager.get(user_id)
        group = group_manager.get(user.group_id)
        right_status = group.has_right(right_name=required_right)
        if not right_status:
            right_status = group.has_extended_right(right_name=required_right)
        return right_status
    except ManagerGetError:
        return False


@deprecated
def insert_request_user(func):
    """helper function which auto injects the user from the token request
    requires: login_required
    """

    @functools.wraps(func)
    def get_request_user(*args, **kwargs):
        from flask import request, current_app
        with current_app.app_context():
            user_manager = UserManager(current_app.database_manager)

        token = parse_authorization_header(request.headers['Authorization'])
        try:
            decrypted_token = TokenValidator().decode_token(token)
        except ValidationError as err:
            return abort(401)
        try:
            user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']
        except ValueError:
            return abort(401)
        user = user_manager.get(user_id)
        kwargs.update({'request_user': user})
        return func(*args, **kwargs)

    return get_request_user


@deprecated
def right_required(required_right: str, excepted: dict = None):
    """wraps function for routes which requires a special user right
    requires: insert_request_user
    """

    with current_app.app_context():
        group_manager = GroupManager(current_app.database_manager, RightManager(rights))

    def _page_right(func):
        @functools.wraps(func)
        def _decorate(*args, **kwargs):
            try:
                current_user: UserModel = kwargs['request_user']
            except KeyError:
                return abort(400, 'No request user was provided')
            try:
                group: UserGroupModel = group_manager.get(current_user.group_id)
                has_right = group.has_right(required_right)
            except ManagerGetError:
                return abort(404, 'Group or right not exists')
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
    value = wsgi_to_bytes(header)
    try:
        auth_type, auth_info = value.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        # Fallback for old versions
        auth_type = b"bearer"
        auth_info = value

    if auth_type == b"basic":
        try:
            username, password = base64.b64decode(auth_info).split(b":", 1)

            with current_app.app_context():
                username = to_unicode(username, "utf-8")
                password = to_unicode(password, "utf-8")

                user_manager: UserManager = UserManager(current_app.database_manager)
                auth_module = AuthModule(SystemSettingsReader(current_app.database_manager))

                try:
                    user_instance = auth_module.login(user_manager, username, password)
                except Exception as e:
                    return None
                if user_instance:
                    tg = TokenGenerator(current_app.database_manager)
                    return tg.generate_token(payload={'user': {
                        'public_id': user_instance.get_public_id()
                    }})
                else:
                    return None
        except Exception:
            return None

    if auth_type == b"bearer":
        try:
            tv = TokenValidator()
            decoded_token = tv.decode_token(auth_info)
            tv.validate_token(decoded_token)
            return auth_info
        except Exception:
            return None
    return None
