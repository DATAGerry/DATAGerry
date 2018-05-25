from flask import Blueprint, current_app, jsonify, abort, request
from cmdb.communication_interface.rest_api.utils import json_required
from cmdb.object_framework import CmdbObject
from cmdb.data_storage.database_manager import NoDocumentFound, DocumentCouldNotBeDeleted
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFound
from bson import json_util
import json

object_rest = Blueprint('object_rest', __name__, url_prefix='/objects')


@object_rest.route('/<int:public_id>', methods=['GET'])
def get_object(public_id):
    try:
        tmp_object = current_app.obm.get_object(public_id)
    except NoDocumentFound:
        abort(404)
    except RequiredInitKeyNotFound:
        abort(406)
    return jsonify(json.loads(json_util.dumps(tmp_object.to_json())))


@object_rest.route('/', methods=['GET'])
def get_all_objects():
    all_objects = current_app.obm.get_all_objects()
    all_json = []
    for obj in all_objects:
        all_json.append(obj.to_json())
    return jsonify(json.loads(json_util.dumps(all_json)))


@json_required
@object_rest.route('/', methods=['POST'])
def add_object():
    try:
        new_object = CmdbObject(**request.json)
        ack = current_app.obm.insert_object(new_object.to_database())
    except RequiredInitKeyNotFound as e:
        abort(406, e.message)
    return jsonify(ack)


@json_required
@object_rest.route('/<int:public_id>', methods=['PUT'])
def update_object(public_id):
    try:
        current_app.obm.get_object(public_id)
        deload = json.loads(json_util.dumps((request.json)), object_hook=json_util.object_hook)
        up_object = CmdbObject(**deload)
        ack = current_app.obm.update_object(up_object.to_database())
    except NoDocumentFound:
        abort(404)
    except RequiredInitKeyNotFound as e:
        abort(406, e.message)
    return jsonify(ack.updatedExisting)


@object_rest.route('/<int:public_id>', methods=['DELETE'])
def delete_object(public_id):
    try:
        ack = current_app.obm.delete_object(public_id)
    except DocumentCouldNotBeDeleted as e:
        abort(400, e.message)
    return jsonify(ack.acknowledged)
