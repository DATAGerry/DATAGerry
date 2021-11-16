# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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


import copy

from pytest import fixture
from datetime import datetime, timezone
from http import HTTPStatus

from cmdb.framework import TypeModel, CmdbObject
from cmdb.framework.models.type import TypeRenderMeta, TypeFieldSection, TypeSummary
from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.sections import GroupACL


@fixture(scope='module')
def example_type():
    return TypeModel(
        public_id=1, name='test', label='Test', author_id=1, creation_time=datetime.now(),
        active=True, version=None, description='Test type',
        render_meta=TypeRenderMeta(
            sections=[
                TypeFieldSection(type='section', name='test-section',
                                 label='TEST', fields=['dummy-field-1', 'dummy-field-2'])
            ],
            summary=TypeSummary(fields=['dummy-field-1'])
        ),
        fields=[{
            "type": "text",
            "name": "dummy-field-1",
            "label": "Test"
        }, {
            "type": "text",
            "name": "dummy-field-2",
            "label": "Test"
        }],
        acl=AccessControlList(activated=False, groups=GroupACL(includes=None))
    )


@fixture(scope='module')
def example_object():
    return CmdbObject(
        public_id=1, type_id=1, status=True, creation_time=datetime.now(timezone.utc),
        author_id=1, active=True, fields=[{
            "name": "dummy-field-1",
            "value": 'dummy-value'
        }, {
            "name": "dummy-field-2",
            "value": ''
        }], version='1.0.0'
    )


@fixture(scope='module')
def change_object() -> dict:
    """
    The 'active' property must be undefined.
    This setting is required for object validation via CmdbObject.SCHEMA Validation
    """
    return {
        "type_id": 1,
        "version": "1.0.1",
        "author_id": 1,
        "fields": [
            {
                "name": "dummy-field-2",
                "value": "dummy-change"
            }
        ],
        "views": 0
    }


@fixture(scope='module')
def collection(connector, database_name):
    from pymongo.mongo_client import MongoClient
    from pymongo.collection import Collection
    client: MongoClient = connector.client
    collection: Collection = client.get_database(database_name).get_collection(TypeModel.COLLECTION)
    return collection


@fixture(scope='module', autouse=True)
def setup(request, collection, example_type):
    collection.insert_one(document=TypeModel.to_json(example_type))

    def drop_collection():
        collection.drop()

    request.addfinalizer(drop_collection)


@fixture(scope='module', autouse=True)
def setup(request, collection, example_type):
    collection.insert_one(document=TypeModel.to_json(example_type))

    def drop_collection():
        collection.drop()

    request.addfinalizer(drop_collection)


class TestBulkChangeFrameworkObjects:

    OBJECT_COLLECTION: str = CmdbObject.COLLECTION
    ROUTE_URL: str = '/object'

    def test_insert_object(self, rest_api, example_object, full_access_user):
        """
        Prepare data for mass change with access control
        """
        i = 0
        while i < 3:
            i = i + 1
            data = copy.copy(CmdbObject.to_json(example_object))
            data['public_id'] = i
            data['active'] = i % 2 != 0
            data['fields'][0]['value'] = f'dummy-value-{i}'
            access_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/', json=data, user=full_access_user)
            assert access_insert_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)

        assert len(rest_api.get(f'{self.ROUTE_URL}/').get_json()['results']) == 3

    def test_bulk_change_object_field_value(self, rest_api, change_object, full_access_user):

        expectations = rest_api.get(f'{self.ROUTE_URL}/').get_json()['results']
        params = {'objectIDs': [1, 2, 3]}

        response = rest_api.put(f'{self.ROUTE_URL}/0', json=change_object, query_string=params, user=full_access_user)
        results: [dict] = response.get_json()['results']

        assert response.status_code == HTTPStatus.ACCEPTED
        assert len(expectations) == len(results)

        # Compare all field values with the change object
        assert change_object['fields'][0] == results[0]['fields'][1]
        assert change_object['fields'][0] == results[1]['fields'][1]
        assert change_object['fields'][0] == results[2]['fields'][1]

        # Compare all field values with the original
        assert results[0]['fields'] != expectations[0]['fields']
        assert results[1]['fields'] != expectations[1]['fields']
        assert results[2]['fields'] != expectations[2]['fields']

        # Compare active state
        assert results[0]['active'] == expectations[0]['active']
        assert results[1]['active'] == expectations[1]['active']
        assert results[2]['active'] == expectations[2]['active']

    def test_bulk_change_object_active_state(self, rest_api, change_object, full_access_user):

        expectations = rest_api.get(f'{self.ROUTE_URL}/').get_json()['results']
        params = {'objectIDs': [1, 2, 3]}

        change_object['active'] = True
        response = rest_api.put(f'{self.ROUTE_URL}/0', json=change_object, query_string=params, user=full_access_user)
        results: [dict] = response.get_json()['results']

        assert response.status_code == HTTPStatus.ACCEPTED
        assert len(expectations) == len(results)

        # Compare active state
        assert results[0]['active']
        assert results[1]['active']
        assert results[2]['active']



