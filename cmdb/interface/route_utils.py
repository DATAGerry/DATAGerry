# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
import functools
import json
from functools import wraps

from authlib.jose.errors import ExpiredTokenError

from cmdb.user_management import User
from cmdb.utils.wraps import LOGGER

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

from flask import Blueprint, request, abort

from cmdb.framework.cmdb_dao import CmdbDAO
from cmdb.security.token.validator import TokenValidator, ValidationError
from cmdb.utils import json_encoding

DEFAULT_MIME_TYPE = 'Content-Type: application/json'


class RootBlueprint(Blueprint):
    """Wrapper class for Blueprints with nested elements"""

    def __init__(self, *args, **kwargs):
        super(RootBlueprint, self).__init__(*args, **kwargs)
        self.nested_blueprints = []

    def register_nested_blueprint(self, nested_blueprint):
        """Add a 'sub' blueprint to root element
        Args:
            nested_blueprint (NestedBlueprint): Blueprint for sub routes
        """
        self.nested_blueprints.append(nested_blueprint)


class NestedBlueprint:
    """Default Blueprint class but with parent prefix route
    """

    def __init__(self, blueprint, url_prefix):
        self.blueprint = blueprint
        self.prefix = '/' + url_prefix
        super(NestedBlueprint, self).__init__()

    def route(self, rule, **options):
        rule = self.prefix + rule
        return self.blueprint.route(rule, **options)


def make_response(instance: (CmdbDAO, list, dict), status_code=200):
    """
    make json http response with indent settings and auto encoding
    Args:
        instance: instance of a cmdbDao instance or instance of the subclass
        status_code: optional status code
    Returns:
        http valid response
    """
    from flask import make_response as flask_response
    # set indent to None of min value exists in the request - DEFAULT: 2 steps
    # indent = None if 'indent' in request.args else 2
    indent = 2
    # encode the dict data from the object to json data
    resp = flask_response(json.dumps(instance, default=json_encoding.default, indent=indent), status_code)
    # add header information
    resp.mimetype = DEFAULT_MIME_TYPE
    return resp


def login_required(f):
    """wraps function for routes which requires an authentication
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """checks if user is logged in and valid
        """
        auth = request.authorization
        if auth is None and 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                tv = TokenValidator()
                decoded_token = tv.decode_token(token)
                tv.validate_token(decoded_token)
            except (ValidationError, ExpiredTokenError, CMDBError) as err:
                LOGGER.error(err)
                return abort(401)
        else:
            return abort(401)
        return f(*args, **kwargs)

    return decorated


def insert_request_user(func):
    """helper function which auto injects the user from the token request
    requires: login_required
    """

    @functools.wraps(func)
    def get_user(*args, **kwargs):
        from flask import request
        from cmdb.user_management.user_manager import user_manager
        token = request.headers['Authorization']
        try:
            decrypted_token = TokenValidator().decode_token(token)
        except ValidationError:
            return abort(401)
        try:
            user_id = decrypted_token['DATAGERRY']['value']['user']['public_id']
        except ValueError:
            return abort(401)
        user = user_manager.get_user(user_id)
        kwargs.update({'request_user': user})
        return func(*args, **kwargs)

    return get_user


def right_required(required_right: str, *args, **kwargs):
    """wraps function for routes which requires a special user right
    requires: insert_request_user
    """

    def _page_right(func):
        @functools.wraps(func)
        def _decorate(*args, **kwargs):
            has_right: bool = False
            from cmdb.user_management.user_manager import user_manager
            try:
                current_user: User = kwargs['request_user']
                has_right = user_manager.group_has_right(current_user.get_group(), required_right)
            except (Exception, CMDBError):
                return abort(403)
            if not has_right:
                return abort(403)
            return func(*args, **kwargs)

        return _decorate

    return _page_right


