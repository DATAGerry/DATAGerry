# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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

import logging

from flask import abort, request, current_app

from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse
from cmdb.manager import ManagerIterationError, ManagerGetError

from cmdb.interface.blueprint import APIBlueprint
from cmdb.docapi.docapi_template.docapi_template import DocapiTemplate
from cmdb.docapi.docapi_template.docapi_template_manager import DocapiTemplateManager

with current_app.app_context():
    docapi_tpl_manager = DocapiTemplateManager(current_app.database_manager, current_app.event_queue)
    object_manager = CmdbObjectManager(current_app.database_manager, current_app.event_queue)

LOGGER = logging.getLogger(__name__)

doc_blueprint = APIBlueprint('doc', __name__)


# DEFAULT ROUTES
@doc_blueprint.route('/template', methods=['GET', 'HEAD'])
@doc_blueprint.protect(auth=True, right='base.docapi.template.view')
@doc_blueprint.parse_collection_parameters()
def get_template_list(params: CollectionParameters):
    template_manager = DocapiTemplateManager(database_manager=current_app.database_manager)
    body = request.method == 'HEAD'

    try:
        iteration_result: IterationResult[DocapiTemplate] = template_manager.get_templates(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        types = [DocapiTemplate.to_json(type) for type in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params,
                                        url=request.url, model=DocapiTemplate.MODEL, body=body)
    except ManagerIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()
