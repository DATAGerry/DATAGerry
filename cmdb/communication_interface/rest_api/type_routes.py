from flask import Blueprint, current_app, jsonify, abort
from cmdb.data_storage.database_manager import NoDocumentFound
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFound
from bson import json_util
import json

type_rest = Blueprint('type_rest', __name__, url_prefix='/types')


@type_rest.route('/<int:public_id>', methods=['GET'])
def get_type(public_id):
    try:
        tmp_type = current_app.obm.get_type(public_id)
    except NoDocumentFound:
        abort(404)
    except RequiredInitKeyNotFound:
        abort(406)
    return jsonify(json.loads(json_util.dumps(tmp_type.to_json())))