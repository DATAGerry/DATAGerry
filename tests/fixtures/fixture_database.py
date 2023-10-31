# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
import pytest

from cmdb.database.connection import MongoConnector
from cmdb.database.managers import DatabaseManagerMongo


@pytest.fixture(scope="session")
def mongodb_parameters(request):
    return request.config.getoption('--mongodb-host'), \
           request.config.getoption('--mongodb-port'), \
           request.config.getoption('--mongodb-database')


@pytest.fixture(scope="session")
def database_name(mongodb_parameters):
    return mongodb_parameters[2]


@pytest.fixture(scope="session")
def connector(mongodb_parameters):
    host, port, database = mongodb_parameters
    return MongoConnector(host, port, database)


@pytest.fixture(scope="session")
def database_manager(mongodb_parameters):
    host, port, database = mongodb_parameters
    return DatabaseManagerMongo(host, port, database)