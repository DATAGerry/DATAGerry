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

import logging
import json

from flask import current_app, abort, request
from cmdb.interface.route_utils import make_response, RootBlueprint, login_required
from cmdb.framework.cmdb_errors import TypeInsertError
from cmdb.framework.cmdb_type import CmdbType

with current_app.app_context():
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
importer_blueprint = RootBlueprint('import_rest', __name__, url_prefix='/import')

with current_app.app_context():
    from cmdb.interface.rest_api.importer.importer_object_routes import importer_object_blueprint
    importer_blueprint.register_nested_blueprint(importer_object_blueprint)


@importer_blueprint.route('/type/', methods=['POST'])
@login_required
def add_type():
    from bson import json_util
    from datetime import datetime

    updload = request.form.get('uploadFile')
    # add_data_dump = json.dumps(upload)
    # try:
    #     new_type_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    #     new_type_data['public_id'] = object_manager.get_new_id(CmdbType.COLLECTION)
    #     new_type_data['creation_time'] = datetime.utcnow()
    # except TypeError as e:
    #     LOGGER.warning(e)
    #     abort(400)

    try:
        data_dump = json.loads(updload, object_hook=json_util.object_hook)
        for add_data_dump in data_dump:
            try:
                type_instance = CmdbType(**add_data_dump)
            except CMDBError as e:
                LOGGER.debug(e)
                return abort(400)
            try:
                ack = object_manager.update_type(type_instance)
            except TypeInsertError:
                return abort(500)

    except CMDBError as e:
        LOGGER.debug(e)
        return abort(400)

    resp = make_response(data_dump)
    return resp