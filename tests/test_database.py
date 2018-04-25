import pytest
import os
from cmdb.data_storage import DatabaseManagerMongo, MongoConnector
from cmdb.data_storage.database_connection import ServerTimeoutError

"""
class TestDatabaseConnection:

    def test_client_connection(self):
        connector = MongoConnector(
            host='127.0.0.1',
            port=27017,
            database_name="cmdb_test",
            timeout=1
        )
        # Check if connection exists
        assert connector.connect()['ok'] == 1.0
        connector.disconnect()
        '''with pytest.raises(ServerTimeoutError):
            connector.connect()'''



class TestDatabaseManager:

    def test_manager_connection(self):
        # check if manager can connect
        test_manager = DatabaseManagerMongo(connector=MongoConnector(
            host='127.0.0.1',
            port=27017,
            database_name='cmdb_test',
            timeout=1
        ))
        assert test_manager.status() is True
"""