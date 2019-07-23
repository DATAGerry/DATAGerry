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

from cmdb.utils.interface_wraps import login_required
from flask import abort, jsonify
from cmdb.object_framework.cmdb_errors import TypeNotFoundError
from cmdb.interface.route_utils import make_response, RootBlueprint
from cmdb.utils.helpers import load_class

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
export_route = RootBlueprint('export_rest', __name__, url_prefix='/export')


@export_route.route('/', methods=['GET'])
@login_required
def get_extension_list():
    # TODO Check which formats are allowed for users
    from cmdb.file_export.file_exporter import FileExporter
    return make_response(FileExporter(None, None, None).get_extension_list())


@export_route.route('<string:collection>/<string:public_ids>/<string:extension>', methods=['GET'])
@login_required
def export_file(collection, public_ids, extension):
    try:
        curr_exporter = load_class('cmdb.file_export.'
                                   + extension + '_file_exporter.'
                                   + extension.capitalize() + 'FileExporter')
        file_export = curr_exporter(collection, extension, public_ids)
        if 'xls' == extension:
            return file_export.main()
        else:
            file_export.main()
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return file_export.export(mime_type='text/' + extension, file_extension=extension)


@export_route.route('/object/type/<int:public_id>/<string:extension>', methods=['GET'])
@login_required
def export_file_by_type_id(public_id, extension):
    try:
        curr_exporter = load_class('cmdb.file_export.'
                                   + extension + '_file_exporter.'
                                   + extension.capitalize() + 'FileExporter')
        file_export = curr_exporter(None, extension, public_id)
        if 'xls' == extension:
            return file_export.main()
        else:
            file_export.main()
    except TypeNotFoundError as e:
        return abort(400, e.message)
    except ModuleNotFoundError as e:
        return abort(400, e)
    except CMDBError as e:
        return abort(404, jsonify(message='Not Found', error=e.message))

    return file_export.export(mime_type='text/' + extension, file_extension=extension)

