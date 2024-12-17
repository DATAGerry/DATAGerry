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
import pytest
from cmdb.interface.cmdb_app import BaseCmdbApp

from cmdb.interface.rest_api.init_rest_api import create_rest_api
from tests.utils.flask_test_client import RestAPITestClient
# -------------------------------------------------------------------------------------------------------------------- #

@pytest.fixture(scope="session")
def rest_api(database_manager, full_access_user):
    """TODO: document"""
    api = create_rest_api(database_manager)
    api.test_client_class = RestAPITestClient

    with api.test_client(database_manager=database_manager, default_auth_user=full_access_user) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def app_context():
    """TODO: document"""
    current_app = BaseCmdbApp(__name__)
    with current_app.app_context():
        yield
