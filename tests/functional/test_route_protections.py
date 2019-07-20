# dataGerry - OpenSource Enterprise CMDB
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

import pytest


@pytest.mark.usefixtures("client", "init_config_reader")
class TestProtectedRoutes:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

    def test_user_protections(self, client, init_config_reader):
        assert client.get('user/').status_code == self.UNAUTHORIZED
        assert client.get('user/1').status_code == self.UNAUTHORIZED
        assert client.get('user/test').status_code == self.UNAUTHORIZED

    def test_group_protections(self, client, init_config_reader):
        assert client.get('group/').status_code == self.UNAUTHORIZED
        assert client.get('group/1').status_code == self.UNAUTHORIZED
        assert client.get('group/').status_code == self.UNAUTHORIZED

    def test_right_protections(self, client, init_config_reader):
        assert client.get('right/').status_code == self.UNAUTHORIZED
        assert client.get('right/tree').status_code == self.UNAUTHORIZED
        assert client.get('right/test').status_code == self.UNAUTHORIZED
        assert client.get('right/level/0').status_code == self.UNAUTHORIZED
        assert client.get('right/levels').status_code == self.UNAUTHORIZED

    def test_object_protections(self, client, init_config_reader):
        assert client.get('object/').status_code == self.UNAUTHORIZED
        assert client.get('object/type/1').status_code == self.UNAUTHORIZED

    def test_type_protections(self, client, init_config_reader):
        assert client.get('type/').status_code == self.UNAUTHORIZED
        assert client.get('type/1').status_code == self.UNAUTHORIZED

    def test_category_protections(self, client, init_config_reader):
        assert client.get('category/').status_code == self.UNAUTHORIZED
        assert client.get('category/tree').status_code == self.UNAUTHORIZED
        assert client.get('category/1').status_code == self.UNAUTHORIZED
