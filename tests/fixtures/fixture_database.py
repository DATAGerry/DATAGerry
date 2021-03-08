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