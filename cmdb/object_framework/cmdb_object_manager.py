"""
This manager represents the core functionalities for the use of CMDB objects.
All communication with the objects is controlled by this manager.
The implementation of the manager used is always realized using the respective superclass.

"""
from cmdb.object_framework import *


class CmdbManagerBase:
    """Represents the base class for object managers. A respective implementation is always adapted to the
       respective database manager :class:`cmdb.data_storage.DatabaseManager` or the used functionalities.
       But should always use at least the super functions listed here.

    """

    def __init__(self, database_manager):
        """Example:
            Depending on the condition or whether a fork process is used, the database manager can also be seen
            directly in the declaration of the object manager

        .. code-block:: python
               :linenos:

                system_config_reader = get_system_config_reader()
                object_manager = CmdbObjectManager(
                    database_manager = DatabaseManagerMongo(
                        connector=MongoConnector(
                            host=system_config_reader.get_value('host', 'Database'),
                            port=int(system_config_reader.get_value('port', 'Database')),
                            database_name=system_config_reader.get_value('database_name', 'Database'),
                            timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
                        )
                    )
                )

        Args:
            database_manager (DatabaseManager): initialisation of an database manager

        """
        if database_manager:
            self.dbm = database_manager

    def _get(self, collection: str, public_id: int) -> str:
        """get document from the database by their public id

        Args:
            collection (str): name of the database collection
            public_id (int): public id of the document/entry

        Returns:
            str: founded document in json format
        """
        return self.dbm.find_one(
            collection=collection,
            public_id=public_id
        )

    def _get_all(self, collection: str, sort='public_id', **requirements: dict) -> list:
        """get all documents from the database which have the passing requirements

        Args:
            collection (str): name of the database collection
            sort (str): sort by given key - default public_id
            **requirements (dict): dictionary of key value requirement

        Returns:
            list: list of all documents

        """
        requirements_filter = {}
        formatted_sort = [(sort, self.dbm.DESCENDING)]
        for k, req in requirements.items():
            requirements_filter.update({k: req})
        return self.dbm.find_all(collection=collection, filter=requirements_filter, sort=formatted_sort)

    def _insert(self, collection: str, data: dict) -> int:
        """insert document/object into database

        Args:
            collection (str): name of the database collection
            data (dict): dictionary of object or the data

        Returns:
            int: new public_id of inserted document
            None: if anything goes wrong

        """
        return self.dbm.insert(
            collection=collection,
            data=data
        )

    def _update(self, collection: str, public_id: int, data: dict):
        return self.dbm.update(
            collection=collection,
            public_id=public_id,
            data=data
        )

    def _delete(self, collection: str, public_id: int):
        return self.dbm.delete(
            collection=collection,
            public_id=public_id
        )


class CmdbObjectManager(CmdbManagerBase):
    def __init__(self, database_manager=None):
        """

        Args:
            database_manager:
        """
        super(CmdbObjectManager, self).__init__(database_manager)

    def get_object(self, public_id: int):
        """get object by public id
        Args:
            public_id:

        Returns:

        """
        return CmdbObject(
            **self._get(
                collection=CmdbObject.COLLECTION,
                public_id=public_id
            )
        )

    def get_objects(self, public_ids: list):
        object_list = []
        for public_id in public_ids:
            object_list.append(self.get_object(public_id))
        return object_list

    def get_objects_by(self, sort='public_id', **requirements: dict):
        ack = []
        objects = self._get_all(collection=CmdbObject.COLLECTION, sort=sort, **requirements)
        for obj in objects:
            ack.append(CmdbObject(**obj))
        return ack

    def get_all_objects(self):
        ack = []
        objects = self.dbm.find_all(collection=CmdbObject.COLLECTION)
        for obj in objects:
            ack.append(CmdbObject(**obj))
        return ack

    def get_objects_by_type(self, type_id: int):
        return self.get_objects_by(type_id=type_id)

    def insert_object(self, data: dict):
        new_object = CmdbObject(**data)
        ack = self.dbm.insert(
            collection=CmdbObject.COLLECTION,
            data=new_object.to_database()
        )
        return ack

    def insert_many_objects(self, objects: list):
        ack = []
        for obj in objects:
            if isinstance(obj, CmdbObject):
                ack.append(self.insert_object(obj.to_database()))
            elif isinstance(obj, dict):
                ack.append(self.insert_object(obj))
            else:
                raise Exception
        return ack

    def update_object(self, data: dict):
        update_object = CmdbObject(**data)
        ack = self.dbm.update(
            collection=CmdbObject.COLLECTION,
            public_id=update_object.get_public_id(),
            data=update_object.to_database()
        )
        return ack

    def update_many_objects(self, objects: list):
        ack = []
        for obj in objects:
            if isinstance(obj, CmdbObject):
                ack.append(self.update_object(obj.to_database()))
            elif isinstance(obj, dict):
                ack.append(self.update_object(obj))
            else:
                raise Exception
        return ack

    def delete_object(self, public_id: int):
        ack = self._delete(CmdbObject.COLLECTION, public_id)
        return ack

    def delete_many_objects(self, public_ids: list):
        ack = []
        for public_id in public_ids:
            if isinstance(public_id, CmdbObject):
                ack.append(self.delete_object(public_id.get_public_id()))
            else:
                ack.append(self.delete_object(public_id))
        return ack

    def get_all_types(self):
        ack = []
        types = self.dbm.find_all(collection=CmdbType.COLLECTION)
        for type_obj in types:
            ack.append(CmdbType(**type_obj))
        return ack

    def get_type(self, public_id: int):
        return CmdbType(**self.dbm.find_one(
            collection=CmdbType.COLLECTION,
            public_id=public_id)
        )

    def insert_type(self, data: dict):
        new_type = CmdbType(**data)
        return self._insert(collection=CmdbType.COLLECTION, data=new_type.to_database())

    def update_type(self, data: dict):
        update_type = CmdbType(**data)
        ack = self.dbm.update(
            collection=CmdbType.COLLECTION,
            public_id=CmdbType.get_public_id(),
            data=update_type.to_database()
        )
        return ack

    def delete_type(self, public_id: int):
        ack = self._delete(CmdbType.COLLECTION, public_id)
        return ack

    def get_all_categories(self):
        ack = []
        cats = self.dbm.find_all(collection=CmdbTypeCategory.COLLECTION)
        for cat_obj in cats:
            ack.append(CmdbTypeCategory(**cat_obj))
        return ack

    def get_category(self, public_id: int):
        return CmdbTypeCategory(**self.dbm.find_one(
            collection=CmdbTypeCategory.COLLECTION,
            public_id=public_id)
        )

    def insert_category(self, data: dict):
        new_category = CmdbTypeCategory(**data)
        return self._insert(collection=CmdbTypeCategory.COLLECTION, data=new_category.to_database())

    def update_category(self, data: dict):
        update_type = CmdbTypeCategory(**data)
        ack = self.dbm.update(
            collection=CmdbTypeCategory.COLLECTION,
            public_id=CmdbTypeCategory.get_public_id(),
            data=update_type.to_database()
        )
        return ack

    def delete_category(self, public_id: int):
        ack = self._delete(CmdbTypeCategory.COLLECTION, public_id)
        return ack
