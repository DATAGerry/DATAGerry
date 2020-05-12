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
from cmdb.docapi.docapi_base import DocApiManager
from cmdb.docapi.docapi_template.docapi_template import DocapiTemplate, DocapiTemplateType

with current_app.app_context():
    docapi_tpl_manager = current_app.docapi_tpl_manager
    object_manager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
docapi_blueprint = RootBlueprint('docapi', __name__, url_prefix='/docapi')


# DEFAULT ROUTES
@docapi_blueprint.route('/', methods=['GET'])
#@login_required
def send_test_document():
    # insert test template
    template = {}
    template['public_id'] = docapi_tpl_manager.get_new_id()
    template['name'] = 'test'
    template['label'] = 'Test'
    template['description'] = 'only a test'
    template['active'] = True
    template['author_id'] = 1
    template['template_data'] = """
        <html>
            <body>
                <h1>DATAGERRY Object #{{ id }}</h1>
                <img src="data:image/png;base64,iVBORw0KGgoAAA
                ANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4
                //8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU
                5ErkJggg==" alt="Red dot" />
                <p style="border: 1px solid">Testdata {{fields['management-hostname']}}</p>
            </body>
        </html>
    """
    template['template_type'] = DocapiTemplateType.OBJECT.name
    template['template_parameters'] = {}
    template_instance = DocapiTemplate(**template)
    public_id = docapi_tpl_manager.insert_template(template_instance)

    # test rendering
    docapi_manager = DocApiManager(docapi_tpl_manager, object_manager)
    output = docapi_manager.render_object_template(public_id, 666)


    # return data
    return Response(
        output,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=output.pdf"
        }
    )
