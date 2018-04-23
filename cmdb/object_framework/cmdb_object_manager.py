from cmdb.data_storage import DATABASE_MANAGER


class CmdbObjectManager:

    def __init__(self, database_manager=None):
        if not database_manager:
            self.dbm = database_manager
        else:
            self.dbm = DATABASE_MANAGER

    def get_object(self, public_id: int):
        pass

    def get_type(self, public_id: int):
        pass

    def get_category(self, public_id: int):
        pass
