# DATAGERRY - OpenSource Enterprise CMDB
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

import logging, json

from flask import abort, jsonify, request
from cmdb.framework.cmdb_errors import TypeNotFoundError
from cmdb.file_export.file_exporter import FileExporter
from cmdb.interface.route_utils import make_response, login_required
from cmdb.interface.blueprint import RootBlueprint
from cmdb.utils.helpers import load_class

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
file_blueprint = RootBlueprint('file_rest', __name__, url_prefix='/file')


@file_blueprint.route('/', methods=['GET'])
@login_required
def get_export_file_types():
    _types = FileExporter.get_type_list()
    _list = []

    for type_element in _types:
        type_element_class = load_class('cmdb.file_export.export_types.' + type_element)
        type_element_properties = {
                'id': type_element,
                'label': type_element_class.LABEL,
                'icon': type_element_class.ICON,
                'multiTypeSupport': type_element_class.MULTITYPE_SUPPORT,
                'helperText': type_element_class.DESCRIPTION,
                'active': type_element_class.ACTIVE
        }
        _list.append(type_element_properties)

    return make_response(_list)


@file_blueprint.route('/object/', methods=['GET'])
@login_required
def export_file():
    try:
        _object_ids = request.args.get('ids', [])
        _class = request.args.get('classname', '')
        _zipping = request.args.get('zip', False) in ['true', 'True']

        if _zipping:
            export_type_class = load_class('cmdb.file_export.export_types.' + 'ZipExportType')()
            file_export = FileExporter('object', export_type_class, _object_ids, _class)
        else:
            export_type_class = load_class('cmdb.file_export.export_types.' + _class)()
            file_export = FileExporter('object', export_type_class, _object_ids)

    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return file_export.export()


@file_blueprint.route('/object/type/<int:public_id>/<string:export_class>', methods=['GET'])
@login_required
def export_file_by_type_id(public_id, export_class):
    try:
        export_type_class = load_class('cmdb.file_export.export_types.' + export_class)
        export_type = export_type_class()
        file_export = FileExporter(None, export_type, public_id)
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return file_export.export()

