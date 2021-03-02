from cmdb import __title__
from cmdb.interface.cmdb_app import BaseCmdbApp
from cmdb.interface.rest_api import create_rest_api


def test_start_routine():
    assert __title__ == 'DATAGERRY'


class TestRestAPI:

    def test_rest_api_start(self, database_manager, rest_api):
        api = create_rest_api(database_manager, None)
        assert isinstance(api, BaseCmdbApp)
        assert rest_api.get('/').get_json()['title'] == __title__
