import logging
from flask import Blueprint, jsonify, request, abort

from cmdb.interface.route_utils import RootBlueprint
from cmdb.interface.rest_api import app

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

settings_rest = RootBlueprint('settings_rest', __name__, url_prefix='/settings')
with app.app_context():
    from cmdb.interface.rest_api.settings.user_management import user_management_routes
    settings_rest.register_nested_blueprint(user_management_routes)
    MANAGER_HOLDER = app.manager_holder


@settings_rest.route('/', methods=['GET'])
def get_settings():
    return "Test"

