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

from cmdb.database.mongo_connector import MongoConnector
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
# -------------------------------------------------------------------------------------------------------------------- #

@pytest.fixture(scope="session", name="mongodb_parameters")
def fixture_mongodb_parameters(request):
    """TODO: document"""
    return request.config.getoption('--mongodb-host'), \
           request.config.getoption('--mongodb-port'), \
           request.config.getoption('--mongodb-database')


@pytest.fixture(scope="session")
def database_name(mongodb_parameters):
    """TODO: document"""
    return mongodb_parameters[2]


@pytest.fixture(scope="session")
def connector(mongodb_parameters):
    """TODO: document"""
    host, port, database = mongodb_parameters
    return MongoConnector(host, port, database)


@pytest.fixture(scope="session")
def database_manager(mongodb_parameters):
    "TODO: document"
    host, port, database = mongodb_parameters
    return DatabaseManagerMongo(host, port, database)
