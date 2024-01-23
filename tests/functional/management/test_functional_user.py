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
from http import HTTPStatus

from flask import Response

from tests.utils.response_tester import default_response_tests
# -------------------------------------------------------------------------------------------------------------------- #

class TestManagementUser:
    """TODO: document"""
    ROUTE_URL = '/users'

    def test_user_iterate(self, rest_api):
        """TODO: document"""
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
        """TODO: document"""
        assert rest_api.get(f'{self.ROUTE_URL}/1').status_code == HTTPStatus.OK
        assert rest_api.get(f'{self.ROUTE_URL}/2').status_code == HTTPStatus.NOT_FOUND

    def test_user_insert(self, rest_api):
        """TODO: document"""
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
        """TODO: document"""
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
        """TODO: document"""
        insert_response: Response = rest_api.delete(f'{self.ROUTE_URL}/2')
        assert insert_response.content_type == 'application/json'
        assert insert_response.status_code == HTTPStatus.ACCEPTED
