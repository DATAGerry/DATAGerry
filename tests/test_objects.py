import pytest
from cmdb.object_framework import CmdbObjectManager


@pytest.fixture
def database_manager(scope='module'):
    import os
    from cmdb.data_storage.database_connection import MongoConnector
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    return DatabaseManagerMongo(
        connector=MongoConnector(
            host=os.environ["TEST_HOST"],
            port=int(os.environ["TEST_PORT"]),
            database_name=os.environ['TEST_DATABASE'],
            timeout=100
        )
    )


@pytest.fixture
def object_manager(database_manager):
    return CmdbObjectManager(
        database_manager=database_manager
    )


def test_object_manager(object_manager):
    assert object_manager.is_ready() is True