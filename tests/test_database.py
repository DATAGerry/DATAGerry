import pytest
import os
from cmdb.data_storage.database_connection import MongoConnector, ServerTimeoutError
from cmdb.data_storage.database_manager import DatabaseManagerMongo, CollectionAlreadyExists


@pytest.fixture
def mongo_connection():
    return MongoConnector(
        host=os.environ["TEST_HOST"],
        port=int(os.environ["TEST_PORT"]),
        database_name=os.environ['TEST_DATABASE'],
        timeout=100
    )


def test_connection(mongo_connection):
    connection = mongo_connection

    assert connection.is_connected() is True
    connection.disconnect()
    assert connection.is_connected() is True

    failed_connection = MongoConnector(
        host=None,
        port=int(os.environ["TEST_PORT"]),
        database_name=os.environ['TEST_DATABASE'],
        timeout=1
    )
    with pytest.raises(ServerTimeoutError):
        failed_connection.connect()


def test_manager(mongo_connection):
    database_manager = DatabaseManagerMongo(mongo_connection)
    database_manager.create("test_database")
    database_manager.create_collection("objects.data")
    with pytest.raises(CollectionAlreadyExists):
        database_manager.create_collection("objects.data")
    database_manager.delete_collection("objects.data")
