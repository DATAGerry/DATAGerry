import pytest

from cmdb.interface.rest_api import create_rest_api
from tests.utils.flask_test_client import RestAPITestClient


@pytest.fixture(scope="session")
def rest_api(database_manager, full_access_user):
    api = create_rest_api(database_manager, None)
    api.test_client_class = RestAPITestClient

    with api.test_client(database_manager=database_manager, default_auth_user=full_access_user) as client:
        yield client
