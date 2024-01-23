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
from json import dumps
from datetime import datetime, timezone
from http import HTTPStatus

from pytest import fixture

from cmdb.framework.models.type_model import TypeSummary
from cmdb.framework import TypeModel, CmdbObject
from cmdb.framework.models.type_model import TypeFieldSection, TypeRenderMeta
from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.sections import GroupACL
# -------------------------------------------------------------------------------------------------------------------- #

@fixture(scope='module')
def example_type():
    """TODO: document"""
    return TypeModel(
        public_id=1, name='test', label='Test', author_id=1, creation_time=datetime.now(),
        active=True, version=None, description='Test type',
        render_meta=TypeRenderMeta(
            sections=[
                TypeFieldSection(type='section', name='test-section', label='TEST', fields=['test-field'])
            ],
            summary=TypeSummary(fields=['test-field'])
        ),
        fields=[{
            "type": "text",
            "name": "test-field",
            "label": "Test"
        }],
        acl=AccessControlList(activated=False, groups=GroupACL(includes=None))
    )


@fixture(scope='module')
def example_object():
    "TODO: document"
    return CmdbObject(
        public_id=1, type_id=1, status=True, creation_time=datetime.now(timezone.utc),
        author_id=1, active=True, fields=[], version='1.0.0'
    )


@fixture(scope='module')
def collection(connector, database_name):
    """TODO: document"""
    from pymongo.mongo_client import MongoClient
    from pymongo.collection import Collection
    mongo_client: MongoClient = connector.client
    type_collection: Collection = mongo_client.get_database(database_name).get_collection(
                                                                             TestFrameworkObjects.TYPE_COLLECTION
                                                                           )
    return type_collection


@fixture(scope='module', autouse=True)
def setup(request, collection, example_type):
    """TODO: document"""
    collection.insert_one(document=TypeModel.to_json(example_type))
    dummy_type = example_type
    dummy_type.public_id = 2
    dummy_type.fields = []
    dummy_type.fields.append({
                             "type": "ref",
                             "name": "test-field",
                             "label": "simple reference field",
                             "ref_types": [1],
                             "summaries": [{
                                 "type_id": 1,
                                 "line": "ReferenceTO: {}",
                                 "label": "ReferenceTO",
                                 "fields": ["test-dummy-field"],
                                 "icon": "fa fa-cube",
                                 "prefix": False
                             }
                             ],
                             "value": ""})
    collection.insert_one(document=TypeModel.to_json(dummy_type))

    def drop_collection():
        collection.drop()

    request.addfinalizer(drop_collection)


class TestFrameworkObjects:
    """TODO: document"""
    OBJECT_COLLECTION: str = CmdbObject.COLLECTION
    TYPE_COLLECTION: str = TypeModel.COLLECTION
    ROUTE_URL: str = '/objects'

    def test_insert_object(self, rest_api, example_object, full_access_user, none_access_user):
        """TODO: document"""
        # Test default
        default_response = rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object))
        assert default_response.status_code == HTTPStatus.OK

        example_object.public_id = 2
        example_object.type_id = 2
        example_object.fields = [{
            "name": "test-field",
            "value": 1,
        }]

        default_response = rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object))
        assert default_response.status_code == HTTPStatus.OK

        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}')
        assert validate_response.status_code == HTTPStatus.OK

        double_check_response = rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object))
        assert double_check_response.status_code == HTTPStatus.BAD_REQUEST

        # DELETE default
        rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}')

        # ACCESS OK
        access_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/',
                                                     json=CmdbObject.to_json(example_object), user=full_access_user)
        assert access_insert_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)

        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}')
        assert validate_response.status_code == HTTPStatus.OK

        # DELETE default
        rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}')

        # ACCESS FORBIDDEN
        forbidden_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object),
                                                        user=none_access_user)
        assert forbidden_insert_types_response.status_code == HTTPStatus.FORBIDDEN

        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}')
        assert validate_response.status_code == HTTPStatus.NOT_FOUND

        # ACCESS UNAUTHORIZED
        un_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object),
                                                 unauthorized=True)
        assert un_insert_types_response.status_code == HTTPStatus.UNAUTHORIZED
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}')

        assert validate_response.status_code == HTTPStatus.NOT_FOUND
        example_object.public_id = 1


    def test_get_objects(self, rest_api, full_access_user, none_access_user):
        """TODO: document"""
        default_response = rest_api.get(f'{self.ROUTE_URL}/')
        assert default_response.status_code == HTTPStatus.OK

        # Response parsable
        response_dict = default_response.get_json()
        test_object_json = response_dict['results'][0]
        test_object = CmdbObject.from_data(test_object_json)

        assert len(response_dict['results']) == int(default_response.headers['X-Total-Count'])
        assert len(response_dict['results'])
        assert isinstance(test_object, CmdbObject)

        # Test filter
        filter_response = rest_api.get(f'{self.ROUTE_URL}/', query_string={'filter': dumps({'public_id': 1})})
        assert filter_response.status_code == HTTPStatus.OK
        assert int(filter_response.headers['X-Total-Count']) == 1

        # Test empty filter
        empty_filter_response = rest_api.get(f'{self.ROUTE_URL}/', query_string={'filter': dumps({'public_id': 2})})
        assert empty_filter_response.status_code == HTTPStatus.OK
        assert int(empty_filter_response.headers['X-Total-Count']) == 0

        # Test wrong filter
        wrong_filter_response = rest_api.get(f'{self.ROUTE_URL}/', query_string={'filter': '\xE9'})
        assert wrong_filter_response.status_code == HTTPStatus.BAD_REQUEST

        # ACCESS OK
        access_get_types_response = rest_api.get(f'{self.ROUTE_URL}/', user=full_access_user)
        assert access_get_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)

        # ACCESS FORBIDDEN
        none_get_types_response = rest_api.get(f'{self.ROUTE_URL}/', user=none_access_user)
        assert none_get_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        none_get_types_response = rest_api.get(f'{self.ROUTE_URL}/', unauthorized=True)
        assert none_get_types_response.status_code == HTTPStatus.UNAUTHORIZED


    def test_get_object(self, rest_api, example_object, full_access_user, none_access_user):
        """TODO: document"""
        default_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}/{"native"}')
        assert default_response.status_code == HTTPStatus.OK

        # Response parsable
        response_dict = default_response.get_json()
        test_object = CmdbObject.from_data(response_dict)
        assert isinstance(test_object, CmdbObject)

        # Not Found
        not_found_response = rest_api.get(f'{self.ROUTE_URL}/{-1}')
        assert not_found_response.status_code == HTTPStatus.NOT_FOUND

        # ACCESS OK
        access_get_types_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}', user=full_access_user)
        assert access_get_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)

        # ACCESS FORBIDDEN
        none_get_types_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}', user=none_access_user)
        assert none_get_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        none_get_types_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}', unauthorized=True)
        assert none_get_types_response.status_code == HTTPStatus.UNAUTHORIZED


    def test_update_object(self, rest_api, example_object, full_access_user, none_access_user):
        """TODO: document"""
        example_object.editor_id = 1
        example_object.creation_time = None

        # Test default
        default_response = rest_api.put(f'{self.ROUTE_URL}/{example_object.public_id}',
                                        json=CmdbObject.to_json(example_object))
        assert default_response.status_code == HTTPStatus.ACCEPTED

        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}/{"native"}')
        assert validate_response.status_code == HTTPStatus.OK

        response_dict = validate_response.get_json()
        test_object = CmdbObject.from_data(response_dict)
        assert isinstance(test_object, CmdbObject)
        assert test_object.last_edit_time is not None

        # ACCESS OK
        access_update_types_response = rest_api.put(f'{self.ROUTE_URL}/{example_object.public_id}',
                                                    json=CmdbObject.to_json(example_object), user=full_access_user)
        assert access_update_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}')
        assert validate_response.status_code == HTTPStatus.OK
        rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}')

        # ACCESS FORBIDDEN
        none_update_types_response = rest_api.put(f'{self.ROUTE_URL}/{example_object.public_id}',
                                                  json=CmdbObject.to_json(example_object), user=none_access_user)
        assert none_update_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        un_get_types_response = rest_api.put(f'{self.ROUTE_URL}/{example_object.public_id}',
                                             json=CmdbObject.to_json(example_object), unauthorized=True)
        assert un_get_types_response.status_code == HTTPStatus.UNAUTHORIZED
        example_object.public_id = 1
        example_object.name = 'test'


    def test_delete_object(self, rest_api, example_object, full_access_user, none_access_user):
        """TODO: document"""
        # Test default route
        rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object))

        default_response = rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}')
        assert default_response.status_code == HTTPStatus.OK

        default_response = rest_api.post(f'{self.ROUTE_URL}/', json=CmdbObject.to_json(example_object))
        assert default_response.status_code == HTTPStatus.OK

        # ACCESS OK
        access_update_types_response = rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}',
                                                       user=full_access_user)
        assert access_update_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_object.public_id}')
        assert validate_response.status_code == HTTPStatus.NOT_FOUND

        # ACCESS FORBIDDEN
        none_update_types_response = rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}',
                                                     user=none_access_user)
        assert none_update_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        un_get_types_response = rest_api.delete(f'{self.ROUTE_URL}/{example_object.public_id}', unauthorized=True)
        assert un_get_types_response.status_code == HTTPStatus.UNAUTHORIZED
