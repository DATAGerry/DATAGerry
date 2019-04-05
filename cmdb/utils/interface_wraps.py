"""
Different wrapper functions for interface module
"""
import logging
from functools import wraps
from flask import request, abort, redirect, url_for, jsonify
from jwcrypto.jwt import JWTExpired, JWTNotYetValid
from jwcrypto.jws import InvalidJWSSignature, InvalidJWSObject

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)


def json_required(f):
    """
    json requirement wrapper
    implements by routes with required an JSON content-type
    Args:
        f: target function

    """

    @wraps(f)
    def _json_required(*args, **kwargs):
        """
        checks if HTTP Content-Type is jso
        TODO: Implement
        """
        if not request or not request.json:
            LOGGER.warn("Not json | {}".format(request))
            abort(400)
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
                from cmdb.interface.rest_api import app
                security_manager = app.get_manager().get_security_manager()
                security_manager.decrypt_token(token)
            except (JWTExpired, JWTNotYetValid, InvalidJWSSignature, InvalidJWSObject):
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
