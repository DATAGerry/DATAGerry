# dataGerry - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import datetime
import time
import json
import csv

from flask import abort, jsonify, Response
from cmdb.object_framework.cmdb_errors import ObjectNotFoundError, TypeNotFoundError
from cmdb.object_framework.cmdb_object_manager import object_manager
from cmdb.utils.interface_wraps import login_required
from cmdb.interface.route_utils import make_response, RootBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
export_route = RootBlueprint('export_rest', __name__, url_prefix='/export')


@login_required
@export_route.route('/csv/<string:collection>/<int:public_id>', methods=['GET'])
def export_csv(collection, public_id):

    data_list = [get_db_result(collection, public_id, None)]
    csv_data = parse_to_csv(data_list)

    return response_file(csv_data, mime_type='text/csv', file_extension='csv')


@login_required
@export_route.route('/csv/<string:collection>/type/<int:type_id>', methods=['GET'])
def export_csv_by_object_type(collection, type_id):

    data_list = get_db_result(collection, None, type_id)
    csv_data = parse_to_csv(data_list)

    return response_file(csv_data, mime_type='text/csv', file_extension='csv')


@login_required
@export_route.route('/json/<string:collection>/<int:public_id>', methods=['GET'])
def export_json(collection, public_id):

    data = get_db_result(collection, public_id, None)
    json_data = make_response(data).data

    return response_file(json_data, mime_type='application/json', file_extension='txt')


@login_required
@export_route.route('/json/<string:collection>/type/<int:type_id>', methods=['GET'])
def export_json_by_object_type(collection, type_id):

    data = get_db_result(collection, None, type_id)
    json_data = make_response(data).data

    return response_file(json_data, mime_type='application/json', file_extension='txt')


@login_required
@export_route.route('/xml/<string:collection>/<int:public_id>', methods=['GET'])
def export_xml(collection, public_id):
    data = get_db_result(collection, public_id, None)
    xml_data = json.loads(make_response(data).data)

    return response_file(parse_to_xml(xml_data), mime_type="text/xml", file_extension="xml")


@login_required
@export_route.route('/xml/<string:collection>/type/<int:type_id>', methods=['GET'])
def export_xml_by_object_type(collection, type_id):
    data = get_db_result(collection, None, type_id)
    xml_data = json.loads(make_response(data).data)

    return response_file(parse_to_xml(xml_data), mime_type="text/xml", file_extension="xml")


def parse_to_xml(json_obj, line_spacing=""):
    result_list = list()
    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(parse_to_xml(sub_elem, line_spacing))
        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_spacing, tag_name))
            result_list.append(parse_to_xml(sub_obj, "\t" + line_spacing))
            result_list.append("%s</%s>" % (line_spacing, tag_name))
        return "\n".join(result_list)
    return "%s%s" % (line_spacing, json_obj)


def parse_to_csv(data_list):
    header = ['public_id']
    rows = [',']
    i = 0
    for obj in data_list:
        fields = obj.fields
        row = [str(obj.public_id)]

        for key in fields:
            if i == 0:
                header.append(key.get('name'))
            row.append(str(key.get('value')))
        rows.append(','.join(row))
        i = i + 1

    return ','.join(header) + '\n'.join(rows)


def get_db_result(collection: str, public_id, type_id):
    try:
        if collection == 'object':
            try:
                if type_id is not None:
                    return object_manager.get_objects_by_type(type_id)
                return object_manager.get_object(public_id)
            except ObjectNotFoundError as e:
                return jsonify(message='Not Found', error=e.message)

        if collection == 'type':
            try:
                return object_manager.get_type(public_id)
            except TypeNotFoundError as e:
                return jsonify(message='Not Found', error=e.message)

    except CMDBError:
        return abort(404)


def response_file(file, mime_type: str, file_extension: str):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H_%M_%S')
    return Response(
        file,
        mimetype=mime_type,
        headers={
            "Content-Disposition":
                "attachment; filename=%s.%s" % (timestamp, file_extension)
        }
    )
