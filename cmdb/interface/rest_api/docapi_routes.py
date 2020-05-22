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

from flask import abort, request, jsonify, current_app, Response
from cmdb.utils.helpers import load_class, get_module_classes
from cmdb.interface.route_utils import make_response, RootBlueprint, login_required, insert_request_user, right_required
from cmdb.docapi.docapi_base import DocApiManager
from cmdb.docapi.docapi_template.docapi_template import DocapiTemplate, DocapiTemplateType
from cmdb.docapi.docapi_template.docapi_template_manager import DocapiTemplateManagerGetError, \
    DocapiTemplateManagerInsertError, DocapiTemplateManagerUpdateError, DocapiTemplateManagerDeleteError
from cmdb.user_management import User

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
@docapi_blueprint.route('/template', methods=['GET'])
@docapi_blueprint.route('/template/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_template_list(request_user: User):
    """
    get all objects in database
    Returns:
        list of docapi templates
    """
    try:
        tpl_list = docapi_tpl_manager.get_all_templates()
    except DocapiTemplateManagerGetError as err:
        return abort(400, err.message)
    except ModuleNotFoundError as err:
        return abort(400, err)
    except CMDBError as err:
        return abort(404, jsonify(message='Not Found', error=err.message))
    return make_response(tpl_list)


@docapi_blueprint.route('/template/<int:public_id>/', methods=['GET'])
@docapi_blueprint.route('/template/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_template(public_id, request_user: User):
    """
        get template in database
        Returns:
            docapi template
        """
    try:
        tpl = docapi_tpl_manager.get_template(public_id)
    except DocapiTemplateManagerGetError as err:
        LOGGER.error(err)
        return abort(404)
    resp = make_response(tpl)
    return resp


@docapi_blueprint.route('/template/<string:name>/', methods=['GET'])
@docapi_blueprint.route('/template/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def get_template_by_name(name: str, request_user: User):
    try:
        tpl = docapi_tpl_manager.get_template_by_name(name=name)
    except DocapiTemplateManagerGetError as err:
        return abort(404, err.message)
    return make_response(tpl)


@docapi_blueprint.route('/template', methods=['POST'])
@docapi_blueprint.route('/template/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.object.add')
def add_template(request_user: User):
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    try:
        new_tpl_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_tpl_data['public_id'] = docapi_tpl_manager.get_new_id()
        new_tpl_data['author_id'] = request_user.get_public_id()
    except TypeError as err:
        LOGGER.warning(err)
        abort(400)
    try:
        template_instance = DocapiTemplate(**new_tpl_data)
    except CMDBError as err:
        LOGGER.debug(err)
        return abort(400)
    try:
        ack = docapi_tpl_manager.insert_template(template_instance)
    except DocapiTemplateManagerInsertError:
        return abort(500)

    resp = make_response(ack)
    return resp


@docapi_blueprint.route('/template', methods=['PUT'])
@docapi_blueprint.route('/template/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.object.edit')
def update_template(request_user: User):
    from bson import json_util
    add_data_dump = json.dumps(request.json)
    new_tpl_data = None
    try:
        new_tpl_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as err:
        LOGGER.warning(err)
        abort(400)
    try:
        update_tpl_instance = DocapiTemplate(**new_tpl_data)
    except CMDBError:
        return abort(400)
    try:
        docapi_tpl_manager.update_template(update_tpl_instance, request_user, False)
    except DocapiTemplateManagerUpdateError:
        return abort(500)
    resp = make_response(update_tpl_instance)
    return resp


@docapi_blueprint.route('/template/<int:public_id>/', methods=['DELETE'])
@docapi_blueprint.route('/template/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.object.delete')
def delete_template(public_id: int, request_user: User):
    try:
        ack = docapi_tpl_manager.delete_template(public_id=public_id, request_user=request_user)
    except DocapiTemplateManagerDeleteError:
        return abort(400)
    except CMDBError:
        return abort(500)
    resp = make_response(ack)
    return resp


@docapi_blueprint.route('/template/<int:public_id>/render/<int:object_id>/', methods=['GET'])
@docapi_blueprint.route('/template/<int:public_id>/render/<int:object_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.delete')
def render_object_template(public_id: int, object_id: int, request_user: User):
    docapi_manager = DocApiManager(docapi_tpl_manager, object_manager)
    output = docapi_manager.render_object_template(public_id, object_id)

    # Todo: error handling

    # return data
    return Response(
        output,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=output.pdf"
        }
    )


@docapi_blueprint.route('/template/testinsert', methods=['GET'])
def insert_test():
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
