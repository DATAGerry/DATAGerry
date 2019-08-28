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

"""
Different wrapper functions for interface module
"""
import logging
from functools import wraps

from flask import request, abort

from cmdb.security.token.validator import TokenValidator, ValidationError

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


def json_required(f):
    @wraps(f)
    def _json_required(*args, **kwargs):
        if not request or not request.json:
            LOGGER.warning("Not json | {}".format(request))
            return abort(400)
        return f(*args, **kwargs)

    return _json_required


def login_required(f):
    """
    Wrapper function for routes which requires an authentication
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """
        checks if user is logged in and valid
        """
        auth = request.authorization

        if auth is None and 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                tv = TokenValidator()
                decoded_token = tv.decode_token(token)
                tv.validate_token(decoded_token)
            except ValidationError as err:
                LOGGER.error(err)
                return abort(401)
            except CMDBError:
                return abort(401)
        else:
            return abort(401)
        return f(*args, **kwargs)

    return decorated


def right_required(required_right: str):
    import json

    def _page_right(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            LOGGER.debug(required_right)
            has_right = False
            from cmdb.interface.rest_api import app
            user_manager = app.get_manager().get_user_manager()
            security_manager = app.get_manager().get_security_manager()
            try:
                user_id = json.loads(security_manager.decrypt_token(request.headers['Authorization']))['public_id']

                has_right = user_manager.user_group_has_right(user_manager.get_user(public_id=user_id), required_right)
                LOGGER.debug(has_right)
            except (Exception, CMDBError):
                abort(403)
            if not has_right:
                abort(403)
            return f(*args, **kwargs)

        return decorated

    return _page_right
