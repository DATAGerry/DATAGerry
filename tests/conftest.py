import pytest

from cmdb.database.connection import MongoConnector
from cmdb.database.errors.database_errors import DatabaseNotExists
from cmdb.database.managers import DatabaseManagerMongo
from cmdb.interface.rest_api import create_rest_api
from cmdb.security.key.generator import KeyGenerator
from cmdb.security.security import SecurityManager
from cmdb.user_management import UserModel
from cmdb.user_management.managers.group_manager import GroupManager
from cmdb.user_management.managers.user_manager import UserManager
from tests.utils.flask_test_client import RestAPITestClient


def pytest_addoption(parser):
    parser.addoption(
        '--mongodb-host', action='store', default='localhost', help='Host of mongodb test instance'
    )
    parser.addoption(
        '--mongodb-port', action='store', default=27017, help='Port of mongodb test instance'
    )
    parser.addoption(
        '--mongodb-database', action='store', default='cmdb-test', help='Database of mongodb test instance'
    )


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


@pytest.fixture(scope="session")
def admin_user():
    return UserModel(
        public_id=1,
        user_name='admin',
        active=True,
        group_id=1
    )


@pytest.fixture(scope="session")
def rest_api(database_manager, admin_user):
    api = create_rest_api(database_manager, None)
    api.test_client_class = RestAPITestClient

    with api.test_client(database_manager=database_manager, default_auth_user=admin_user) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def preset_database(database_manager, database_name):
    try:
        database_manager.drop_database(database_name)
    except DatabaseNotExists:
        pass
    from cmdb.user_management import __FIXED_GROUPS__
    from datetime import datetime

    kg = KeyGenerator(database_manager=database_manager)
    kg.generate_rsa_keypair()
    kg.generate_symmetric_aes_key()

    group_manager = GroupManager(database_manager=database_manager)
    user_manager = UserManager(database_manager=database_manager)
    security_manager = SecurityManager(database_manager=database_manager)

    for group in __FIXED_GROUPS__:
        group_manager.insert(group)

    admin_name = 'admin'
    admin_pass = 'admin'
    admin_user = UserModel(
        public_id=1,
        user_name=admin_name,
        active=True,
        group_id=__FIXED_GROUPS__[0].public_id,
        registration_time=datetime.now(),
        password=security_manager.generate_hmac(admin_pass),
    )
    user_manager.insert(admin_user)
