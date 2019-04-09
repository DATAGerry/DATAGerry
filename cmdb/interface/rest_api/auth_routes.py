import logging
from cmdb import __MODE__
from flask import Blueprint, jsonify, request, abort, current_app

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

auth_routes = Blueprint('auth_rest', __name__, url_prefix='/auth')
LOGGER = logging.getLogger(__name__)

if __MODE__ == 'TESTING':
    MANAGER_HOLDER = None
else:
    with current_app.app_context():
        MANAGER_HOLDER = current_app.get_manager()


@auth_routes.route('/login', methods=['POST'])
def login_call():
    login_data = request.json
    LOGGER.debug(f"Login try for user {login_data['user_name']}")
    login_user = None
    login_user_name = login_data['user_name']
    login_password = login_data['password']
    correct = False
    try:
        login_user = MANAGER_HOLDER.get_user_manager().get_user_by_name(login_user_name)
        auth_method = MANAGER_HOLDER.get_user_manager().get_authentication_provider(login_user.get_authenticator())
        correct = auth_method.authenticate(
            user=login_user,
            password=login_password
        )
    except CMDBError as e:
        abort(401, e)
    if correct:
        return jsonify(MANAGER_HOLDER.get_security_manager().encrypt_token(login_user))
    abort(401)
