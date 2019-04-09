import logging
from flask import Blueprint, make_response, jsonify, current_app
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

connection_routes = Blueprint('connection_routes', __name__)
LOGGER = logging.getLogger(__name__)

with current_app.app_context():
    MANAGER_HOLDER = current_app.get_manager()


@connection_routes.route('/')
def connection_response():
    from cmdb import __title__, __version__

    resp = make_response(jsonify({
        'title': __title__,
        'version': __version__,
        'connected': MANAGER_HOLDER.get_database_manager().status()
    }))
    resp.mimetype = "application/json"
    return resp
