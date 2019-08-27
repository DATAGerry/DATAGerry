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

from werkzeug.exceptions import abort

from cmdb.framework.cmdb_object_manager import object_manager, ObjectManagerGetError
from cmdb.interface.route_utils import RootBlueprint, make_response, NestedBlueprint

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
collection_routes = RootBlueprint('collection_rest', __name__, url_prefix='/collection')
collection_template_routes = NestedBlueprint(collection_routes, url_prefix='/template')


@collection_routes.route('/', methods=['GET'])
def get_collections():
    try:
        collections = object_manager.get_collections()
    except ObjectManagerGetError:
        return abort(404)
    if len(collections) < 1:
        return make_response(collections, 204)
    return make_response(collections)


@collection_routes.route('/<int:public_id>', methods=['GET'])
@collection_routes.route('/<int:public_id>/', methods=['GET'])
def get_collection(public_id: int):
    try:
        collection = object_manager.get_collection(public_id)
    except ObjectManagerGetError:
        return abort(404)
    return make_response(collection)


@collection_routes.route('/', methods=['POST'])
def add_collection():
    raise NotImplementedError


@collection_routes.route('/', methods=['PUT'])
def update_collection():
    raise NotImplementedError


@collection_routes.route('/<int:public_id>/', methods=['DELETE'])
@collection_routes.route('/<int:public_id>', methods=['DELETE'])
def delete_collection(public_id: int):
    raise NotImplementedError


@collection_template_routes.route('/', methods=['GET'])
def get_collection_templates():
    try:
        collection_templates = object_manager.get_collection_templates()
    except ObjectManagerGetError:
        return abort(404)

    if len(collection_templates) < 1:
        return make_response(collection_templates, 204)
    return make_response(collection_templates)


@collection_template_routes.route('/<int:public_id>', methods=['GET'])
@collection_template_routes.route('/<int:public_id>/', methods=['GET'])
def get_collection_template(public_id: int):
    try:
        collection_template = object_manager.get_collection_template(public_id)
    except ObjectManagerGetError:
        return abort(404)
    return make_response(collection_template)


@collection_template_routes.route('/', methods=['POST'])
def add_collection_template():
    raise NotImplementedError


@collection_template_routes.route('/', methods=['PUT'])
def update_collection_template():
    raise NotImplementedError


@collection_template_routes.route('/<int:public_id>/', methods=['DELETE'])
@collection_template_routes.route('/<int:public_id>', methods=['DELETE'])
def delete_collection_template(public_id: int):
    raise NotImplementedError
