import pytest
from cmdb.object_framework.cmdb_object import CmdbObject
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFound
from cmdb.object_framework.cmdb_object_manager import CmdbObjectManager
from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.data_storage.database_connection import MongoConnector


@pytest.fixture(scope='session', autouse=True)
def cmdb_manager():
    cmdb_man = CmdbObjectManager(
        database_manager=DatabaseManagerMongo(
            connector=MongoConnector(
                host='127.0.0.1',
                port=27017,
                database_name="cmdb_test",
                timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
            )
        )
    )
    return cmdb_man


@pytest.fixture(scope="module")
def cmdb_init():
    init_values = {
        "public_id": 1,
        "type_id": 1,
        "active": True,
        "version": "1.0.0",
        "views": 100,
        "fields": [
            {
                "name": "Test 1",
                "value": "Value 1"
            },
            {
                "name": "Test 2",
                "value": "Value 2"
            },
        ],
        "creation_time": "2017-11-18T13:53:02.000+0000",
        "last_edit_time": "2017-05-23T16:36:35.000+0000",
        "status": "Development",
        "logs": None,
        "creator_id": 1,
        "last_editor_id": 1
    }
    return init_values


@pytest.fixture(scope="module")
def cmdb_object(cmdb_init):
    try:
        return CmdbObject(**cmdb_init)
    except RequiredInitKeyNotFound as riknf:
        print(riknf.message)


def test_init_required(cmdb_object, cmdb_init):
    assert isinstance(cmdb_object, CmdbObject)
    assert cmdb_object.__dict__ == cmdb_init

