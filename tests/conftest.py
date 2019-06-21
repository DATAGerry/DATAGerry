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
from cmdb.interface.rest_api import create_rest_api
from tests.unit.test_security_keys import key_holder, key_dir

pytest_plugins = 'tests/pytest_plugins/pytest_mongodb'


@pytest.fixture
def client():
    app = create_rest_api(None)
    app.config.testing = True
    app.debug = True

    return app.test_client()
