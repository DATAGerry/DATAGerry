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

from flask import abort, jsonify, current_app, Response
from cmdb.utils.helpers import load_class, get_module_classes
from cmdb.interface.route_utils import make_response, RootBlueprint, login_required
from cmdb.document_api.documentapi_base import DocumentApiManager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
document_api = RootBlueprint('document_api', __name__, url_prefix='/documentapi')


# DEFAULT ROUTES
@document_api.route('/', methods=['GET'])
#@login_required
def send_test_document():
    docapi_manager = DocumentApiManager()
    output = docapi_manager.create_doc()
    return Response(
        output,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=output.pdf"
        }
    )
