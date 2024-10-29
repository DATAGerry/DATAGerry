
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
from cmdb import __title__
from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.rest_api.init_rest_api import create_rest_api
# -------------------------------------------------------------------------------------------------------------------- #

def test_start_routine():
    """TODO: document"""
    assert __title__ == 'DATAGERRY'


class TestRestAPI:
    """TODO: document"""

    def test_rest_api_start(self, database_manager, rest_api):
        """TODO: document"""
        api = create_rest_api(database_manager, None)
        assert isinstance(api, BaseCmdbApp)
        assert rest_api.get('/').get_json()['title'] == __title__
