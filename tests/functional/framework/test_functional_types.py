from json import dumps

from pytest import fixture, importorskip
from datetime import datetime
from http import HTTPStatus

from cmdb.framework import TypeModel
from cmdb.framework.models.type import TypeRenderMeta, TypeFieldSection, TypeSummary
from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.sections import GroupACL
from tests.utils.flask_test_client import RestAPITestSuite


@fixture(scope='module')
def example_type():
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
def collection(connector, database_name):
    from pymongo.mongo_client import MongoClient
    from pymongo.collection import Collection
    mongo_client: MongoClient = connector.client
    collection: Collection = mongo_client.get_database(database_name).get_collection(TestFrameworkTypes.COLLECTION)
    return collection


@fixture(scope='module', autouse=True)
def setup(request, collection, example_type):
    collection.insert_one(document=TypeModel.to_json(example_type))

    def drop_collection():
        collection.drop()

    request.addfinalizer(drop_collection)


class TestFrameworkTypes(RestAPITestSuite):
    importorskip('cmdb.framework')

    COLLECTION: str = TypeModel.COLLECTION
    ROUTE_URL: str = '/types'

    def test_get_types(self, rest_api, full_access_user, none_access_user):
        # Route callable
        default_response = rest_api.get(f'{self.ROUTE_URL}/')
        assert default_response.status_code == HTTPStatus.OK

        # Response parsable
        response_dict = default_response.get_json()
        test_type_json = response_dict['results'][0]
        test_type = TypeModel.from_data(test_type_json)

        assert len(response_dict['results']) == int(default_response.headers['X-Total-Count'])
        assert len(response_dict['results'])
        assert isinstance(test_type, TypeModel)

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

    def test_get_type(self, rest_api, example_type, full_access_user, none_access_user):
        # Route callable
        default_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert default_response.status_code == HTTPStatus.OK

        # Response parsable
        response_dict = default_response.get_json()
        test_type_json = response_dict['result']
        test_type = TypeModel.from_data(test_type_json)
        assert isinstance(test_type, TypeModel)

        # Not Found
        not_found_response = rest_api.get(f'{self.ROUTE_URL}/{-1}')
        assert not_found_response.status_code == HTTPStatus.NOT_FOUND

        # ACCESS OK
        access_get_types_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}', user=full_access_user)
        assert access_get_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)

        # ACCESS FORBIDDEN
        none_get_types_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}', user=none_access_user)
        assert none_get_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        none_get_types_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}', unauthorized=True)
        assert none_get_types_response.status_code == HTTPStatus.UNAUTHORIZED

    def test_insert_type(self, rest_api, example_type, full_access_user, none_access_user):
        example_type.public_id = 2
        example_type.name = 'test2'

        # Test default route
        default_response = rest_api.post(f'{self.ROUTE_URL}/', json=TypeModel.to_json(example_type))
        assert default_response.status_code == HTTPStatus.CREATED
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.OK
        double_check_response = rest_api.post(f'{self.ROUTE_URL}/', json=TypeModel.to_json(example_type))
        assert double_check_response.status_code == HTTPStatus.BAD_REQUEST
        rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}')

        # ACCESS OK
        access_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/',
                                                     json=TypeModel.to_json(example_type), user=full_access_user)
        assert access_insert_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.OK
        rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}')

        # ACCESS FORBIDDEN
        forbidden_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/', json=TypeModel.to_json(example_type),
                                                        user=none_access_user)
        assert forbidden_insert_types_response.status_code == HTTPStatus.FORBIDDEN
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.NOT_FOUND

        # ACCESS UNAUTHORIZED
        un_insert_types_response = rest_api.post(f'{self.ROUTE_URL}/', json=TypeModel.to_json(example_type),
                                                 unauthorized=True)
        assert un_insert_types_response.status_code == HTTPStatus.UNAUTHORIZED
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.NOT_FOUND
        example_type.public_id = 1
        example_type.name = 'test'

    def test_update_type(self, rest_api, example_type, full_access_user, none_access_user):
        example_type.name = 'updated'

        # Test default route
        default_response = rest_api.put(f'{self.ROUTE_URL}/{example_type.public_id}',
                                        json=TypeModel.to_json(example_type))
        assert default_response.status_code == HTTPStatus.ACCEPTED

        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.OK
        assert validate_response.get_json()['result']['name'] == 'updated'

        # ACCESS OK
        access_update_types_response = rest_api.put(f'{self.ROUTE_URL}/{example_type.public_id}',
                                                    json=TypeModel.to_json(example_type), user=full_access_user)
        assert access_update_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.OK
        rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}')

        # ACCESS FORBIDDEN
        none_update_types_response = rest_api.put(f'{self.ROUTE_URL}/{example_type.public_id}',
                                                  json=TypeModel.to_json(example_type), user=none_access_user)
        assert none_update_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        un_get_types_response = rest_api.put(f'{self.ROUTE_URL}/{example_type.public_id}',
                                             json=TypeModel.to_json(example_type), unauthorized=True)
        assert un_get_types_response.status_code == HTTPStatus.UNAUTHORIZED
        example_type.public_id = 1
        example_type.name = 'test'

    def test_delete_type(self, rest_api, example_type, full_access_user, none_access_user):
        # Test default route
        rest_api.post(f'{self.ROUTE_URL}/', json=TypeModel.to_json(example_type))

        default_response = rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert default_response.status_code == HTTPStatus.ACCEPTED

        default_response = rest_api.post(f'{self.ROUTE_URL}/', json=TypeModel.to_json(example_type))
        assert default_response.status_code == HTTPStatus.CREATED

        # ACCESS OK
        access_update_types_response = rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}',
                                                       user=full_access_user)
        assert access_update_types_response.status_code != (HTTPStatus.FORBIDDEN or HTTPStatus.UNAUTHORIZED)
        validate_response = rest_api.get(f'{self.ROUTE_URL}/{example_type.public_id}')
        assert validate_response.status_code == HTTPStatus.NOT_FOUND

        # ACCESS FORBIDDEN
        none_update_types_response = rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}',
                                                     user=none_access_user)
        assert none_update_types_response.status_code == HTTPStatus.FORBIDDEN

        # ACCESS UNAUTHORIZED
        un_get_types_response = rest_api.delete(f'{self.ROUTE_URL}/{example_type.public_id}', unauthorized=True)
        assert un_get_types_response.status_code == HTTPStatus.UNAUTHORIZED

