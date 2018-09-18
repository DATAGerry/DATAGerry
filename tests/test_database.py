import pytest
import os
from cmdb.utils.error import CMDBError
from cmdb.data_storage.database_connection import MongoConnector
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

    failed_connection = MongoConnector(
        host=None,
        port=int(os.environ["TEST_PORT"]),
        database_name=os.environ['TEST_DATABASE'],
        timeout=1
    )
    # with pytest.raises(ServerTimeoutError):
    #    failed_connection.connect()


def test_manager(mongo_connection):
    database_manager = DatabaseManagerMongo(mongo_connection)
    database_manager.create("test_database")
    database_manager.create_collection("objects.data")
    with pytest.raises(CollectionAlreadyExists):
        database_manager.create_collection("objects.data")
    database_manager.delete_collection("objects.data")


def test_database_collection_init(mongo_connection):
    database_manager = DatabaseManagerMongo(mongo_connection)
    database_manager.setup()
    from cmdb.object_framework import __COLLECTIONS__ as OB_COLLECTIONS
    from cmdb.user_management import __COLLECTIONS__ as MM_COLLECTIONS
    __COLLECTIONS__ = OB_COLLECTIONS + MM_COLLECTIONS
    col_names = []
    for col_name in __COLLECTIONS__:
        col_names.append(col_name.COLLECTION)
    col_names.sort()
    db_col_names = database_manager.database_connector.get_collections()
    db_col_names.sort()
    assert col_names == db_col_names
    for col_name in db_col_names:
        database_manager.delete_collection(col_name)
    assert len(database_manager.database_connector.get_collections()) == 0

