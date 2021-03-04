from http import HTTPStatus

from flask import Response

from tests.utils.response_tester import default_response_tests


class TestManagementUser:
    ROUTE_URL = '/users'

    def test_user_iterate(self, rest_api):
        get_response: Response = rest_api.get(f'{self.ROUTE_URL}/')
        default_response_tests(get_response)
        get_response_data: dict = get_response.get_json()
        assert get_response_data['count'] == 1
        assert get_response_data['total'] == 1

        get_response_400: Response = rest_api.get(f'{self.ROUTE_URL}/', query_string={'filter': '\xE9'})
        assert get_response_400.status_code == 400

        head_response: Response = rest_api.head(f'{self.ROUTE_URL}/')
        default_response_tests(head_response)

    def test_user_get(self, rest_api):
        assert rest_api.get(f'{self.ROUTE_URL}/1').status_code == HTTPStatus.OK
        assert rest_api.get(f'{self.ROUTE_URL}/2').status_code == HTTPStatus.NOT_FOUND

    def test_user_insert(self, rest_api):
        test_user = {
            'public_id': 2,
            'user_name': 'test',
            'active': True,
            'group_id': 1,
            'password': 'test'
        }
        insert_response: Response = rest_api.post(f'{self.ROUTE_URL}/', json=test_user)
        assert insert_response.content_type == 'application/json'
        assert insert_response.status_code == HTTPStatus.CREATED

    def test_user_update(self, rest_api):
        test_user = {
            'public_id': 2,
            'user_name': 'test',
            'active': True,
            'group_id': 1,
            'password': 'test2'
        }
        insert_response: Response = rest_api.put(f'{self.ROUTE_URL}/2', json=test_user)
        assert insert_response.content_type == 'application/json'
        assert insert_response.status_code == HTTPStatus.ACCEPTED

    def test_user_delete(self, rest_api):
        insert_response: Response = rest_api.delete(f'{self.ROUTE_URL}/2')
        assert insert_response.content_type == 'application/json'
        assert insert_response.status_code == HTTPStatus.ACCEPTED
