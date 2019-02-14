"""
Different wrapper functions for interface module
"""
from functools import wraps
from flask import request, abort, redirect, url_for
from cmdb.utils.logger import get_logger
from jwcrypto.jwt import JWTExpired, JWTNotYetValid
from jwcrypto.jws import InvalidJWSSignature, InvalidJWSObject
from cmdb.user_management import User

LOGGER = get_logger()


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
        if 'access-token' in request.cookies:
            token = request.cookies['access-token']
        else:
            return redirect(url_for('auth_pages.login_page'))
        try:
            from flask import current_app
            security_manager = current_app.manager_holder.get_security_manager()
            security_manager.decrypt_token(token)
        except (JWTExpired, JWTNotYetValid, InvalidJWSSignature, InvalidJWSObject) as e:
            return redirect(url_for('auth_pages.login_page', error=e))
        except Exception as e:
            return redirect(url_for('auth_pages.login_page', error=e))
        return f(*args, **kwargs)

    return decorated


def right_required(required_right: str):
    """
    TODO: FIX


    def page_right(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from cmdb.interface.web_app import MANAGER_HOLDER
            usm = MANAGER_HOLDER.get_user_manager()

            right = usm.get_right(required_right)
            LOGGER.debug(right)
            security_manager = MANAGER_HOLDER.get_security_manager()
            user = User(security_manager.decrypt_token(request.cookies.get('access-token')))
            try:
                ack_right = usm.user_has_right(user, required_right)
                LOGGER.debug(ack_right)
            except Exception:
                abort(401)
                return redirect(url_for('static_pages.error_404_page'))
            return f(*args, **kwargs)

        return decorated
    """
    return None
