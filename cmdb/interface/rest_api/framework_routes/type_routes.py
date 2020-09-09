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

from cmdb.framework.models.type import TypeModel
from cmdb.framework.managers import ManagerGetError, ManagerInsertError, ManagerUpdateError, ManagerDeleteError
from cmdb.framework.managers.error.framework_errors import FrameworkIterationError
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.managers.type_manager import TypeManager
from cmdb.framework.utils import PublicID
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse, GetSingleResponse, InsertSingleResponse, UpdateSingleResponse, \
    DeleteSingleResponse

LOGGER = logging.getLogger(__name__)
types_blueprint = APIBlueprint('types', __name__)


@types_blueprint.route('/', methods=['GET', 'HEAD'])
@types_blueprint.protect(auth=True, right='base.framework.type.view')
@types_blueprint.parse_collection_parameters()
def get_types(params: CollectionParameters):
    type_manager = TypeManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        iteration_result: IterationResult[TypeModel] = type_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        types = [TypeModel.to_json(type) for type in iteration_result.results]
        api_response = GetMultiResponse(types, total=iteration_result.total, params=params,
                                        url=request.url, model=TypeModel.MODEL, body=body)
    except FrameworkIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()


@types_blueprint.route('/<int:public_id>', methods=['GET', 'HEAD'])
@types_blueprint.protect(auth=True, right='base.framework.type.view')
def get_type(public_id: int):
    type_manager = TypeManager(database_manager=current_app.database_manager)
    body = True if not request.method != 'HEAD' else False

    try:
        type_ = type_manager.get(public_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    api_response = GetSingleResponse(TypeModel.to_json(type_), url=request.url,
                                     model=TypeModel.MODEL, body=body)
    return api_response.make_response()


@types_blueprint.route('/', methods=['POST'])
@types_blueprint.protect(auth=True, right='base.framework.type.add')
@types_blueprint.validate(TypeModel.SCHEMA)
def insert_type(data: dict):
    type_manager = TypeManager(database_manager=current_app.database_manager)
    try:
        result_id: PublicID = type_manager.insert(data)
        raw_doc = type_manager.get(public_id=result_id)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerInsertError as err:
        return abort(400, err.message)
    api_response = InsertSingleResponse(result_id, raw=TypeModel.to_json(raw_doc), url=request.url,
                                        model=TypeModel.MODEL)
    return api_response.make_response(prefix='types')


@types_blueprint.route('/<int:public_id>', methods=['PUT', 'PATCH'])
@types_blueprint.protect(auth=True, right='base.framework.type.edit')
@types_blueprint.validate(TypeModel.SCHEMA)
def update_type(public_id: int, data: dict):
    type_manager = TypeManager(database_manager=current_app.database_manager)
    try:
        type = TypeModel.from_data(data=data)
        type_manager.update(public_id=PublicID(public_id), type=TypeModel.to_json(type))
        api_response = UpdateSingleResponse(result=data, url=request.url, model=TypeModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerUpdateError as err:
        return abort(400, err.message)

    return api_response.make_response()


@types_blueprint.route('/<int:public_id>', methods=['DELETE'])
@types_blueprint.protect(auth=True, right='base.framework.type.delete')
def delete_type(public_id: int):
    type_manager = TypeManager(database_manager=current_app.database_manager)
    try:
        deleted_type = type_manager.delete(public_id=PublicID(public_id))
        api_response = DeleteSingleResponse(raw=TypeModel.to_json(deleted_type), model=TypeModel.MODEL)
    except ManagerGetError as err:
        return abort(404, err.message)
    except ManagerDeleteError as err:
        return abort(400, err.message)
    return api_response.make_response()
