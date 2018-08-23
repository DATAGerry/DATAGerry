import pytest
import json
from cmdb.interface.rest_api import create_rest_api


@pytest.fixture(scope="function")
def json_object():
    with open('fixtures/objects.data.json') as f:
        data = json.load(f)
    return data


@pytest.fixture(scope='module')
def http_server():
    server = create_rest_api()
    testing_server = server.test_client()
    ctx = server.app_context()
    ctx.push()
    yield testing_server
    ctx.pop()


def test_add_object(http_server, json_object):
    pass
    #response = http_server.post('/objects/', data=json_object, mimetype='application/json')


def test_error_page_not_found(http_server):
    import string
    import random
    response = http_server.get('/'+''.join(random.choice(string.ascii_letters) for i in range(6)))
    assert response.status_code == 404
