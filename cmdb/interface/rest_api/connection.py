import logging
from flask import Blueprint, make_response, jsonify
from cmdb.data_storage import get_pre_init_database
try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

connection_routes = Blueprint('connection_routes', __name__)
LOGGER = logging.getLogger(__name__)


@connection_routes.route('/')
def connection_response():
    from cmdb import __title__, __version__

    resp = make_response(jsonify({
        'title': __title__,
        'version': __version__,
        'connected': get_pre_init_database().status()
    }))
    resp.mimetype = "application/json"
    return resp
