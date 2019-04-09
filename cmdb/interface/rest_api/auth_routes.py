import logging
from cmdb.user_management.user_manager import user_manager
from cmdb.data_storage import get_pre_init_database
from cmdb.utils import get_security_manager
from flask import Blueprint, jsonify, request, abort

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

auth_routes = Blueprint('auth_rest', __name__, url_prefix='/auth')
LOGGER = logging.getLogger(__name__)


@auth_routes.route('/login', methods=['POST'])
def login_call():
    login_data = request.json

    LOGGER.debug(f"Login try for user {login_data['user_name']}")
    login_user = None
    login_user_name = login_data['user_name']
    login_password = login_data['password']
    correct = False
    try:
        login_user = user_manager.get_user_by_name(login_user_name)
        auth_method = user_manager.get_authentication_provider(login_user.get_authenticator())
        correct = auth_method.authenticate(
            user=login_user,
            password=login_password
        )
    except CMDBError as e:
        abort(401, e)
    if correct:
        return jsonify(get_security_manager(get_pre_init_database()).encrypt_token(login_user))
    abort(401)
