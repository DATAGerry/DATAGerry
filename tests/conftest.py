
import pytest
from cmdb.interface.rest_api import create_rest_api

pytest_plugins = 'tests/pytest_plugins/pytest_mongodb'


@pytest.fixture
def client():
    app = create_rest_api(None)
    app.config.testing = True
    app.debug = True

    return app.test_client()
