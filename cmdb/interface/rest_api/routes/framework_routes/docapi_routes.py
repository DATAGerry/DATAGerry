# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""TODO: document"""
import logging
import json
from bson import json_util
from flask import abort, request, Response

from cmdb.manager.manager_provider_model.manager_provider import ManagerProvider
from cmdb.manager.manager_provider_model.manager_type_enum import ManagerType
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.manager.docapi_templates_manager import DocapiTemplatesManager
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.framework.docapi.docapi_renderer import DocApiRenderer
from cmdb.framework.docapi.docapi_template.docapi_template import DocapiTemplate
from cmdb.framework.results import IterationResult
from cmdb.interface.rest_api.responses.response_parameters.collection_parameters import CollectionParameters
from cmdb.interface.rest_api.responses import GetMultiResponse, DefaultResponse
from cmdb.interface.route_utils import login_required, insert_request_user, right_required
from cmdb.interface.blueprints import APIBlueprint, RootBlueprint
from cmdb.models.user_model.user import UserModel

from cmdb.errors.docapi import DocapiGetError, DocapiInsertError, DocapiUpdateError, DocapiDeleteError
from cmdb.errors.manager import ManagerIterationError, ManagerGetError
# -------------------------------------------------------------------------------------------------------------------- #
LOGGER = logging.getLogger(__name__)

docapi_blueprint = RootBlueprint('docapi', __name__, url_prefix='/docapi')
docs_blueprint = APIBlueprint('docs', __name__)
# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

@docapi_blueprint.route('/template', methods=['POST'])
@docapi_blueprint.route('/template/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.docapi.template.add')
def add_template(request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                     request_user)

    add_data_dump = json.dumps(request.json)

    try:
        new_tpl_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
        new_tpl_data['public_id'] = docapi_manager.get_new_docapi_public_id()
        new_tpl_data['author_id'] = request_user.get_public_id()
    except TypeError as err:
        LOGGER.warning(err)
        abort(400)

    try:
        template_instance = DocapiTemplate(**new_tpl_data)
    except Exception as err:
        #TODO: ERROR-FIX
        LOGGER.debug(str(err))
        return abort(400)

    try:
        ack = docapi_manager.insert_template(template_instance)
    except DocapiInsertError as err:
        LOGGER.debug("[add_template] DocapiInsertError: %s", err.message)
        return abort(500, "An error occured when trying to insert the template!")

    api_response = DefaultResponse(ack)

    return api_response.make_response()

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

@docs_blueprint.route('/template', methods=['GET', 'HEAD'])
@insert_request_user
@docs_blueprint.protect(auth=True, right='base.docapi.template.view')
@docs_blueprint.parse_collection_parameters()
def get_template_list(params: CollectionParameters, request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                    request_user)

    try:
        builder_params = BuilderParameters(**CollectionParameters.get_builder_params(params))

        iteration_result: IterationResult[DocapiTemplate] = docapi_manager.get_templates(builder_params)

        types = [DocapiTemplate.to_json(type) for type in iteration_result.results]

        api_response = GetMultiResponse(types,
                                        total=iteration_result.total,
                                        params=params,
                                        url=request.url,
                                        body=request.method == 'HEAD')
    except ManagerIterationError:
        #TODO: ERROR-FIX
        return abort(400)
    except ManagerGetError:
        return abort(404, "Could not retrieve template list!")

    return api_response.make_response()


@docapi_blueprint.route('/template/by/<string:searchfilter>/', methods=['GET'])
@docapi_blueprint.route('/template/by/<string:searchfilter>', methods=['GET'])
@insert_request_user
@login_required
@right_required('base.docapi.template.view')
def get_template_list_filtered(searchfilter: str, request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                         request_user)

    try:
        filterdict = json.loads(searchfilter)
    except Exception as err:
        LOGGER.debug("[get_template_list_filtered] Error: %s, Type: %s", err, type(err))
        return abort(404, f"Could not unpack the search filter: {searchfilter}")

    try:
        tpl = docapi_manager.get_templates_by(**filterdict)
    except DocapiGetError as err:
        LOGGER.debug("[get_template_list_filtered] Error: %s, Type: %s", err, type(err))
        return abort(404, f"Could not retrieve template list for filter: {searchfilter}")

    api_response = DefaultResponse(tpl)

    return api_response.make_response()


@docapi_blueprint.route('/template/<int:public_id>/', methods=['GET'])
@docapi_blueprint.route('/template/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.docapi.template.view')
def get_template(public_id, request_user: UserModel):
    """
    TODO: document
    """
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                         request_user)

    try:
        tpl = docapi_manager.get_template(public_id)
    except DocapiGetError as err:
        LOGGER.debug("DocapiGetError: %s", err.message)
        return abort(404, f"Could not retrieve template with ID: {public_id}!")

    api_response = DefaultResponse(tpl)

    return api_response.make_response()


@docapi_blueprint.route('/template/name/<string:name>/', methods=['GET'])
@docapi_blueprint.route('/template/name/<string:name>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.docapi.template.view')
def get_template_by_name(name: str, request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                            request_user)

    try:
        tpl = docapi_manager.get_template_by_name(name=name)
    except DocapiGetError as err:
        LOGGER.debug("DocapiGetError: %s", err.message)
        return abort(404, f"Could not retrieve template with name: {name}!")

    api_response = DefaultResponse(tpl)

    return api_response.make_response()

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

@docapi_blueprint.route('/template', methods=['PUT'])
@docapi_blueprint.route('/template/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.docapi.template.edit')
def update_template(request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                            request_user)

    add_data_dump = json.dumps(request.json)
    new_tpl_data = None

    try:
        new_tpl_data = json.loads(add_data_dump, object_hook=json_util.object_hook)
    except TypeError as err:
        LOGGER.warning(err)
        abort(400)

    try:
        update_tpl_instance = DocapiTemplate(**new_tpl_data)
    except Exception:
        #TODO: ERROR-FIX
        return abort(400)

    try:
        docapi_manager.update_template(update_tpl_instance)
    except DocapiUpdateError as err:
        LOGGER.debug("[update_template] DocapiUpdateError: %s", err.message)
        return abort(500, "Could not update the template!")

    api_response = DefaultResponse(update_tpl_instance)

    return api_response.make_response()

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

@docapi_blueprint.route('/template/<int:public_id>/', methods=['DELETE'])
@docapi_blueprint.route('/template/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.docapi.template.delete')
def delete_template(public_id: int, request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                            request_user)

    try:
        ack = docapi_manager.delete_template(public_id)
    except DocapiDeleteError as err:
        LOGGER.debug("[delete_template] DocapiDeleteError: %s", err.message)
        return abort(400, f"Could not delete the template with ID:{public_id}!")

    api_response = DefaultResponse(ack)

    return api_response.make_response()


@docapi_blueprint.route('/template/<int:public_id>/render/<int:object_id>/', methods=['GET'])
@docapi_blueprint.route('/template/<int:public_id>/render/<int:object_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.object.view')
def render_object_template(public_id: int, object_id: int, request_user: UserModel):
    """TODO: document"""
    docapi_manager: DocapiTemplatesManager = ManagerProvider.get_manager(ManagerType.DOCAPI_TEMPLATES_MANAGER,
                                                                            request_user)
    objects_manager: ObjectsManager = ManagerProvider.get_manager(ManagerType.OBJECTS_MANAGER, request_user)

    docapi_renderer = DocApiRenderer(objects_manager, docapi_manager)
    output = docapi_renderer.render_object_template(public_id, object_id)

    # return data
    return Response(
        output,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=output.pdf"
        }
    )
