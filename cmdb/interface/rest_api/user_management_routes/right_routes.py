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


from flask import request, abort

from cmdb.framework.managers import ManagerGetError
from cmdb.framework.managers.error.framework_errors import FrameworkIterationError
from cmdb.framework.results import IterationResult
from cmdb.interface.api_parameters import CollectionParameters
from cmdb.interface.blueprint import APIBlueprint
from cmdb.interface.response import GetMultiResponse
from cmdb.user_management.managers.right_manager import RightManager
from cmdb.user_management.models.right import BaseRight
from cmdb.user_management.rights import __all__ as right_tree

rights_blueprint = APIBlueprint('rights', __name__)


@rights_blueprint.route('/', methods=['GET', 'HEAD'])
@rights_blueprint.protect(auth=False, right=None)
@rights_blueprint.parse_collection_parameters(sort='name')
def get_rights(params: CollectionParameters):
    right_manager = RightManager(right_tree)
    body = request.method == 'HEAD'

    try:
        iteration_result: IterationResult[BaseRight] = right_manager.iterate(
            filter=params.filter, limit=params.limit, skip=params.skip, sort=params.sort, order=params.order)
        rights = [BaseRight.to_dict(type) for type in iteration_result.results]
        api_response = GetMultiResponse(rights, total=iteration_result.total, params=params,
                                        url=request.url, model='Right', body=body)
    except FrameworkIterationError as err:
        return abort(400, err.message)
    except ManagerGetError as err:
        return abort(404, err.message)
    return api_response.make_response()
