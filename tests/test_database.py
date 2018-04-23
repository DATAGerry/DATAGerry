import pytest
import os
from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
from cmdb.data_storage.database_connection import ServerTimeoutError


class TestDatabaseConnection:

    def test_client_connection(self):
        connector = MongoConnector(
            host=os.environ['DATABASE_HOST'],
            port=int(os.environ['DATABASE_PORT']),
            database_name='test',
            timeout=1
        )
        # Check if connection exists
        assert connector.connect()['ok'] == 1.0
        connector.disconnect()
        with pytest.raises(ServerTimeoutError):
            connector.connect()


class TestDatabaseManager:

    def test_manager_connection(self):
        # check if manager can connect
        test_manager = DatabaseManagerMongo(connector=MongoConnector(
            host=os.environ['DATABASE_HOST'],
            port=int(os.environ['DATABASE_PORT']),
            database_name='test',
            timeout=1
        ))
        assert test_manager.status() is True
