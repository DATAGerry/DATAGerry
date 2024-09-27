# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2024 becon GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Database Management instance for database actions
"""
import logging
from pymongo.results import DeleteResult, UpdateResult

from cmdb.database.database_manager import DatabaseManager

from cmdb.framework.section_templates.section_template_creator import SectionTemplateCreator
from cmdb.database.mongo_connector import MongoConnector
from cmdb.database.counter import PublicIDCounter
from cmdb.database.utils import DESCENDING

from cmdb.errors.database import NoDocumentFound, DocumentCouldNotBeDeleted
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

class DatabaseManagerMongo(DatabaseManager):
    """
    PyMongo (MongoDB) implementation of Database Manager
    Extends: DatabaseManager
    """

    def __init__(self, host: str, port: int, database_name: str, **kwargs):
        connector = MongoConnector(host, port, database_name, kwargs)
        super().__init__(connector)


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Auto disconnect the database connection when the Manager get destroyed"""
        self.connector.disconnect()


    def setup(self) -> bool:
        """
        Setup script

        Returns:
            acknowledged
        """
        from cmdb.framework import __COLLECTIONS__ as FRAMEWORK_COLLECTIONS
        from cmdb.user_management import __COLLECTIONS__ as USER_MANAGEMENT_COLLECTIONS
        collection = FRAMEWORK_COLLECTIONS + USER_MANAGEMENT_COLLECTIONS

        def _gen_default_tables(collection_class):
            #TODO: Check list_collection_names()-function
            all_collections = self.connector.list_collection_names()

            if collection_class not in all_collections:
                self.create_collection(collection_class.COLLECTION)
                self.create_indexes(collection_class.COLLECTION, collection_class.SUPER_INDEX_KEYS)
                if len(collection_class.INDEX_KEYS) > 0:
                    self.create_indexes(collection_class.COLLECTION, collection_class.INDEX_KEYS)

        for coll in collection:
            # generating the default database "tables"
            try:
                _gen_default_tables(coll)
            except Exception:
                return False
        return True

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert(self, collection: str, data: dict, skip_public: bool = False) -> int:
        """Adds document to database

        Args:
            collection (str): name of database collection
            data (dict): insert data
            skip_public (bool): Skip the public id creation and counter increment
        Returns:
            int: New public id of the document
        """
        if skip_public:
            return self.get_collection(collection).insert_one(data)

        if 'public_id' not in data:
            data['public_id'] = self.get_next_public_id(collection)

        self.get_collection(collection).insert_one(data)
        self.update_public_id_counter(collection, data['public_id'])

        return data['public_id']


    def _init_public_id_counter(self, collection: str):
        """TODO:document"""
        docs_count = self.get_highest_id(collection)
        self.get_collection(PublicIDCounter.COLLECTION).insert_one({
            '_id': collection,
            'counter': docs_count
        })

        return docs_count

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update(self, collection: str, filter: dict, data: dict, *args, **kwargs):
        """
        Update document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter of document
            data: data to update

        Returns:
            acknowledged
        """
        formatted_data = {'$set': data}

        return self.get_collection(collection).update_one(filter, formatted_data, *args, **kwargs)


    def unset_update_many(self, collection: str, filter: dict, data: str, *args, **kwargs):
        """update document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter of document
            data: data to delete

        Returns:
            acknowledged
        """
        formatted_data = {'$unset': {data: 1}}

        return self.get_collection(collection).update_many(filter, formatted_data, *args, **kwargs)


    def update_many(self, collection: str, query: dict, update: dict, add_to_set:bool = False) -> UpdateResult:
        """update all documents that match the filter from a collection.

        Args:
            collection (str): name of database collection
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            A boolean acknowledged as true if the operation ran with write
            concern or false if write concern was disabled
        """
        formatted_data = {'$addToSet':update} if add_to_set else {'$set':update}

        result = self.get_collection(collection).update_many(filter=query, update=formatted_data)

        if not result.acknowledged:
            #TODO: ERROR-FIX
            raise DocumentCouldNotBeDeleted(collection)

        return result


    def increment_public_id_counter(self, collection: str):
        """TODO: document"""
        working_collection = self.get_collection(PublicIDCounter.COLLECTION)
        query = {
            '_id': collection
        }
        counter_doc = working_collection.find_one(query)
        counter_doc['counter'] = counter_doc['counter'] + 1

        try:
            self.get_collection(PublicIDCounter.COLLECTION).update_one(
                                                                query, {'$set':{'counter':counter_doc['counter']}}
                                                            )
        except Exception as error:
            LOGGER.info('Public ID Counter not increased: reason => %s',error)


    def update_public_id_counter(self, collection: str, value: int):
        """TODO: document"""
        working_collection = self.get_collection(PublicIDCounter.COLLECTION)
        query = {
            '_id': collection
        }
        counter_doc = working_collection.find_one(query)
        # init counter, if it was not found
        if counter_doc is None:
            self._init_public_id_counter(collection)
            counter_doc = working_collection.find_one(query)
        # update counter only, if value is higher than counter
        if value > counter_doc['counter']:
            counter_doc['counter'] = value

            formatted_data = {'$set':counter_doc}

            self.get_collection(PublicIDCounter.COLLECTION).update_one(query, formatted_data)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def find_all(self, collection, *args, **kwargs) -> list:
        """calls find with all returns

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            list: list of found documents
        """
        found_documents = self.find(collection=collection, *args, **kwargs)
        return list(found_documents)


    def find(self, collection: str, *args, **kwargs):
        """General find function"""
        if 'projection' not in kwargs:
            kwargs.update({'projection': {'_id': 0}})

        return self.get_collection(collection).find(*args, **kwargs)


    def find_one_by(self, collection: str, *args, **kwargs) -> dict:
        """find one specific document by special requirements
        Args:
            collection (str): name of database collection
        Returns:
            found document
        """
        cursor_result = self.find(collection, limit=1, *args, **kwargs)

        for result in cursor_result.limit(-1):
            return result

        raise NoDocumentFound(collection)


    def find_one(self, collection: str, public_id: int, *args, **kwargs):
        """
        Retrieves a single document with the given public_id from the given collection 

        Args:
            collection (str): name of database collection
            public_id (int): public_id of document

        Returns:
            document with given public_id
        """
        cursor_result = self.find(collection, {'public_id': public_id}, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result


    def find_one_by_object(self, collection: str, object_id: int, *args, **kwargs):
        """
        Retrieves a single document with the given object_id from the given collection

        Args:
            collection (str): name of database collection
            object_id (int): object_id of document

        Returns:
            document with given object_id
        """
        cursor_result = self.find(collection, {'object_id': object_id}, limit=1, *args, **kwargs)
        for result in cursor_result.limit(-1):
            return result


    def count(self, collection: str, filter: dict = None, *args, **kwargs):
        """Count documents based on filter parameters.

        Args:
            collection (str): name of database collection
            filter (dict): document count requirements
            *args: arguments for search operation
            **kwargs:

        Returns:
            returns the count of the documents
        """
        filter = filter or {}
        return self.get_collection(collection).count_documents(filter=filter, *args, **kwargs)


    def aggregate(self, collection: str, *args, **kwargs):
        """
        Aggregation on mongodb.

        Args:
            collection (str): name of database collection
            *args: arguments for search operation
            **kwargs: key arguments

        Returns:
            returns computed results
        """
        return self.get_collection(collection).aggregate(*args, **kwargs, allowDiskUse=True)


    def get_highest_id(self, collection: str) -> int:
        """wrapper function
        calls get_document_with_highest_id() and returns the public_id

        Args:
            collection (str): name of database collection

        Returns:
            int: highest public id
        """
        try:
            formatted_sort = [('public_id', DESCENDING)]

            highest_id = self.find_one_by(collection=collection, sort=formatted_sort)

            highest = int(highest_id['public_id'])
        except NoDocumentFound:
            return 0
        return highest


    def get_next_public_id(self, collection: str) -> int:
        """TODO: document"""
        try:
            found_counter = self.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})
            new_id = found_counter['counter'] + 1
        except (NoDocumentFound, Exception):
            docs_count = self._init_public_id_counter(collection)
            new_id = docs_count + 1
        finally:
            self.increment_public_id_counter(collection)

        return new_id

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete(self, collection: str, filter: dict, *args, **kwargs) -> DeleteResult:
        """delete document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter query

        Returns:
            acknowledged
        """
        result = self.get_collection(collection).delete_one(filter)

        if result.deleted_count != 1:
            #TODO: ERROR-FIX
            raise DocumentCouldNotBeDeleted(collection)

        return result


    def delete_many(self, collection: str, **requirements: dict) -> DeleteResult:
        """removes all documents that match the filter from a collection.

        Args:
            collection (str): name of database collection
            filter (dict): Specifies deletion criteria using query operators.

        Returns:
            A boolean acknowledged as true if the operation ran
            with write concern or false if write concern was disabled
        """
        requirements_filter = {}
        for k, req in requirements.items():
            requirements_filter.update({k: req})

        result = self.get_collection(collection).delete_many(requirements_filter)

        if not result.acknowledged:
            #TODO: ERROR-FIX
            raise DocumentCouldNotBeDeleted(collection)

        return result

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 CHECK ROUTINE SECTION                                                #
# -------------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------- CmdbLocation - SECTION ---------------------------------------------- #

    def get_root_location_data(self) -> dict:
        """
        This class holds the correct root location data
        
        Returns:
            (dict): Returns valid root location data
        """
        return {
            "public_id":1,
            "name":"Root",
            "parent":0,
            "object_id":0,
            "type_id":0,
            "type_label":"Root",
            "type_icon":"fas fa-globe",
            "type_selectable":True
        }


    def validate_root_location(self, tested_location: dict) -> bool:
        """
        Checks if a given location holds valid root location data

        Args:
            tested_location (dict): location data which should be tested

        Returns:
            (bool): Returns boolean if the given dict has valid root location data
        """
        root_location = self.get_root_location_data()

        for root_key, root_value in root_location.items():
            if root_key not in tested_location.keys():
                return False

            # check if value is valid
            if root_value != tested_location[root_key]:
                return False

        return True


    def set_root_location(self, collection: str, create: bool = False):
        """
        Does the setup for root location. If no counter for locations exist, it will be created

        Args:
            collection (str): framework.locations
            create (bool): If true the root location will be created, else it will be updated

        Returns:
            status: status of location creation or update
        """
        status:int = 0

        if create:
            ## check if counter is created in db, else create one
            counter = self.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})

            if not counter:
                self._init_public_id_counter(collection)

            status = self.insert(collection, self.get_root_location_data())
        else:
            status = self.update(collection,{'public_id':1},self.get_root_location_data())

        return status

# ------------------------------------------- CmdbSectionTemplate - Section ------------------------------------------ #

    def init_predefined_templates(self, collection):
        """
        Checks if all predefined templates are created, else create them
        """
        ## check if counter is created in db, else create one
        counter = self.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})

        if not counter:
            self._init_public_id_counter(collection)

        predefined_template_creator = SectionTemplateCreator()
        predefined_templates: list[dict] = predefined_template_creator.get_predefined_templates()

        for predefined_template in predefined_templates:
            # First check if template already exists
            template_name = predefined_template['name']

            result = self.get_collection(collection).find_one(filter={'name':template_name})

            if not result:
                # The template does not exist, create it
                LOGGER.info("Creating Template: %s", {template_name})
                self.insert(collection, predefined_template)
