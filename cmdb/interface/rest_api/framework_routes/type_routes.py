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

from flask import abort, request, current_app

from cmdb.framework.manager import ManagerGetError
from cmdb.framework.manager.error.framework_errors import FrameworkIterationError
from cmdb.framework.manager.results import IterationResult
from cmdb.framework.manager.type_manager import TypeManager
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.response import GetMultiResponse, GetSingleResponse
from cmdb.interface.blueprint import APIBlueprint
from cmdb.framework.dao.type import TypeDAO

LOGGER = logging.getLogger(__name__)
types_blueprint = APIBlueprint('types', __name__)


@types_blueprint.route('/', methods=['GET', 'HEAD'])
@types_blueprint.protect(auth=True, right='base.framework.type.view')
@types_blueprint.parse_collection_parameters()
def get_types(params: CollectionParameters):
    type_manager: TypeManager = TypeManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        iteration_result: IterationResult[TypeDAO] = type_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        types = [TypeDAO.to_json(category) for category in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params, url=request.url,
                                        model=TypeDAO.MODEL, body=body)
    except FrameworkIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@types_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@types_blueprint.protect(auth=True, right='base.framework.type.view')
def get_type(public_id: int):
    type_manager: TypeManager = TypeManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        types = type_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(TypeDAO.to_json(types), url=request.url, model=TypeDAO.MODEL, body=body)
    return api_response.make_response()
