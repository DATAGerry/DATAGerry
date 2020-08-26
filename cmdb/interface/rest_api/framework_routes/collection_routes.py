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
from typing import List

from werkzeug.exceptions import abort
from flask import current_app, request

from cmdb.framework import CmdbCollectionTemplate
from cmdb.framework.cmdb_errors import ObjectManagerGetError, ObjectManagerInsertError
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.interface.route_utils import make_response, login_required, \
    insert_request_user, right_required
from cmdb.interface.blueprint import RootBlueprint, NestedBlueprint
from cmdb.user_management import User

with current_app.app_context():
    object_manager: CmdbObjectManager = current_app.object_manager

try:
    from cmdb.utils.error import CMDBError
except ImportError:
    CMDBError = Exception

LOGGER = logging.getLogger(__name__)
collection_blueprint = RootBlueprint('collection_rest', __name__, url_prefix='/collection')
collection_template_routes = NestedBlueprint(collection_blueprint, url_prefix='/template')
collection_blueprint.register_nested_blueprint(collection_template_routes)


@collection_blueprint.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.collection.view')
def get_collections(request_user: User):
    """Get all collections
    Returns:
        list of all collections
    """
    try:
        collections = object_manager.get_collections()
    except ObjectManagerGetError:
        return abort(404)
    if len(collections) < 1:
        return make_response([], 204)
    return make_response(collections)


@collection_blueprint.route('/<int:public_id>/', methods=['GET'])
@collection_blueprint.route('/<int:public_id>', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.collection.view')
def get_collection(public_id: int, request_user: User):
    try:
        collection = object_manager.get_collection(public_id)
    except ObjectManagerGetError:
        return abort(404)
    return make_response(collection)


@collection_blueprint.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.collection.add')
def add_collection(request_user: User):
    raise NotImplementedError


@collection_blueprint.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.collection.edit')
def update_collection(request_user: User):
    raise NotImplementedError


@collection_blueprint.route('/<int:public_id>/', methods=['DELETE'])
@collection_blueprint.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.collection.delete')
def delete_collection(public_id: int, request_user: User):
    raise NotImplementedError


@collection_template_routes.route('/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.collection.view')
def get_collection_templates(request_user: User):
    try:
        collection_templates: List[CmdbCollectionTemplate] = object_manager.get_collection_templates()
    except ObjectManagerGetError:
        return abort(404)
    if len(collection_templates) < 1:
        return make_response([], 204)
    return make_response(collection_templates)


@collection_template_routes.route('/<int:public_id>', methods=['GET'])
@collection_template_routes.route('/<int:public_id>/', methods=['GET'])
@login_required
@insert_request_user
@right_required('base.framework.collection.view')
def get_collection_template(public_id: int, request_user: User):
    try:
        collection_template: CmdbCollectionTemplate = object_manager.get_collection_template(public_id)
    except ObjectManagerGetError as err:
        return abort(404, err.message)
    return make_response(collection_template)


@collection_template_routes.route('/', methods=['POST'])
@login_required
@insert_request_user
@right_required('base.framework.collection.add')
def add_collection_template(request_user: User):
    collection_template_data = request.json
    if not collection_template_data:
        return abort(400, 'No data was provided')
    try:
        inserted_collection_id: int = object_manager.insert_collection_template(collection_template_data)
    except ObjectManagerInsertError as err:
        LOGGER.error(f'[CollectionTemplate] Error while adding a new collection template: {err.message}')
        return abort(400, err.message)
    return make_response(inserted_collection_id)


@collection_template_routes.route('/', methods=['PUT'])
@login_required
@insert_request_user
@right_required('base.framework.collection.edit')
def update_collection_template(request_user: User):
    raise NotImplementedError


@collection_template_routes.route('/<int:public_id>/', methods=['DELETE'])
@collection_template_routes.route('/<int:public_id>', methods=['DELETE'])
@login_required
@insert_request_user
@right_required('base.framework.collection.delete')
def delete_collection_template(public_id: int, request_user: User):
    raise NotImplementedError
