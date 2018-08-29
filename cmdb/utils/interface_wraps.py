from functools import wraps
from flask import request, abort, redirect, url_for
from cmdb.utils.logger import get_logger
LOGGER = get_logger()


def json_required(f):
    @wraps(f)
    def _json_required(*args, **kwargs):
        LOGGER.warn(request)
        if not request or not request.json:
            abort(400)
        return f(*args, **kwargs)
    return _json_required


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.cookies:
            token = request.cookies.get('access-token')
        else:
            return redirect(url_for('auth_pages.login_page'))
        return f(*args, **kwargs)
    return decorated


def right_required(required_right):
    """
    See Also: https: // stackoverflow.com / questions / 5929107 / decorators -
    with-parameters
        https: // www.artima.com / weblogs / viewpost.jsp?thread = 240845"""

    def page_right(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from cmdb.user_management import UserManagement
            token_payload = token_manager.get_payload(request.cookies.get('access-token'))
            user = user_manager.get_user_by_id(token_payload['public_id'])
            try:
                user_manager.user_has_right(user, required_right)
            except UserHasNotRequiredRight as unr:
                application_logger.warning(unr.message)
                abort(403)
                return redirect(url_for('static_pages.error_404_page'))
            return f(*args, **kwargs)

        return decorated

    return page_right