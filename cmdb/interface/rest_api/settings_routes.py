import logging
from cmdb import __MODE__
from flask import current_app
from cmdb.interface.route_utils import RootBlueprint

LOGGER = logging.getLogger(__name__)
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

settings_rest = RootBlueprint('settings_rest', __name__, url_prefix='/settings')

if __MODE__ == 'TESTING':
    MANAGER_HOLDER = None
else:
    with current_app.app_context():
        from cmdb.interface.rest_api.settings.user_management import user_management_routes

        settings_rest.register_nested_blueprint(user_management_routes)
        MANAGER_HOLDER = current_app.get_manager()


@settings_rest.route('/', methods=['GET'])
def get_settings():
    return "Test"
