from cmdb.object_framework import *
from cmdb.object_framework.cmdb_dao import RequiredInitKeyNotFound


class CmdbObjectManager:

    def __init__(self, database_manager):
        if database_manager:
            self.dbm = database_manager
        else:
            from cmdb.data_storage import DATABASE_MANAGER
            self.dbm = DATABASE_MANAGER

    def get_object(self, public_id: int):
        return CmdbObject(**self.dbm.find_one(
            collection=CmdbObject.COLLECTION,
            public_id=public_id
        ))
