import pytest
import cmdb
from cmdb.interface.rest_api import create_rest_api


@pytest.fixture(scope='module')
def http_server():
    cmdb.__MODE__ = 'TESTING'
    server = create_rest_api()
    testing_server = server.test_client()
    ctx = server.app_context()
    ctx.push()
    yield testing_server
    ctx.pop()


def test_error_page_not_found(http_server):
    import string
    import random
    response = http_server.get('/'+''.join(random.choice(string.ascii_letters) for i in range(6)))
    assert response.status_code == 404
