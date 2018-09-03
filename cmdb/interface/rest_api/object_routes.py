from flask import Blueprint, current_app, jsonify, abort, request
from cmdb.utils.interface_wraps import json_required
from cmdb.object_framework import CmdbObject
from cmdb.data_storage.database_manager import NoDocumentFound, DocumentCouldNotBeDeleted
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFoundError
from bson import json_util
import json
from cmdb.interface.web_app import MANAGER_HOLDER

object_rest = Blueprint('object_rest', __name__, url_prefix='/objects')


@object_rest.route('/<int:public_id>', methods=['GET'])
def get_object(public_id):
    try:
        tmp_object = MANAGER_HOLDER.get_object_manager().get_object(public_id)
    except NoDocumentFound:
        abort(404)
    except RequiredInitKeyNotFoundError:
        abort(406)
    return jsonify(json.loads(json_util.dumps(tmp_object.to_json())))


@json_required
@object_rest.route('/', methods=['POST'])
def add_object():
    from cmdb.data_storage.database_manager import PublicIDAlreadyExists
    try:
        new_object = CmdbObject(**request.json)
        try:
            ack = MANAGER_HOLDER.get_object_manager().insert_object(new_object.to_database())
        except PublicIDAlreadyExists as e:
            abort(409, e, e.message)
    except RequiredInitKeyNotFoundError as e:
        abort(406, e.message)
    except Exception as e:
        abort(406, e)
    return jsonify(ack)


@json_required
@object_rest.route('/<int:public_id>', methods=['PUT'])
def update_object(public_id):
    try:
        MANAGER_HOLDER.get_object_manager().get_object(public_id)
        deload = json.loads(json_util.dumps((request.json)), object_hook=json_util.object_hook)
        up_object = CmdbObject(**deload)
        ack = MANAGER_HOLDER.get_object_manager().update_object(up_object.to_database())
    except NoDocumentFound:
        abort(404)
    except RequiredInitKeyNotFoundError as e:
        abort(406, e.message)
    return jsonify(ack.updatedExisting)


@object_rest.route('/<int:public_id>', methods=['DELETE'])
def delete_object(public_id):
    try:
        ack = MANAGER_HOLDER.get_object_manager().delete_object(public_id)
    except DocumentCouldNotBeDeleted as e:
        abort(400, e.message)
    return jsonify(ack.acknowledged)
