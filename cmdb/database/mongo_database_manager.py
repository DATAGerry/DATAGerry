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
from cmdb.database.mongo_connector import MongoConnector
from cmdb.database.counter import PublicIDCounter

from cmdb.framework.section_templates.section_template_creator import SectionTemplateCreator

from cmdb.errors.database import (
    NoDocumentFound,
    DocumentDeleteError,
    DocumentCreateError,
    DocumentUpdateError,
    DocumentGetError,
    DocumentAggregationError,
)
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                             MongoDatabaseManager - CLASS                                             #
# -------------------------------------------------------------------------------------------------------------------- #
class MongoDatabaseManager(DatabaseManager):
    """
    PyMongo (MongoDB) implementation of Database Manager
    Extends: DatabaseManager
    """
    def __init__(self, host: str, port: int, database_name: str, **kwargs):
        connector = MongoConnector(host, port, database_name, kwargs)
        super().__init__(connector)


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Auto disconnect the database connection when the manager get destroyed
        """
        self.connector.disconnect()

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert(self, collection: str, data: dict, skip_public: bool = False) -> int:
        """
        Adds a document to a collection

        Args:
            collection (str): name of database collection
            data (dict): data which should be inserted
            skip_public (bool): Skip the public id creation and counter increment

        Raises:
            DocumentCreateError: When a document could not be created
        
        Returns:
            int: New public id of the document
        """
        try:
            if skip_public:
                return self.get_collection(collection).insert_one(data)

            if 'public_id' not in data:
                data['public_id'] = self.get_next_public_id(collection)

            self.get_collection(collection).insert_one(data)
            self.update_public_id_counter(collection, data['public_id'])

            return data['public_id']
        except Exception as err:
            LOGGER.debug("[insert] Can't insert document. Error: %s", err)
            raise DocumentCreateError(collection, str(err)) from err


    def __init_public_id_counter(self, collection: str):
        """TODO:document"""
        docs_count = self.get_highest_id(collection)

        self.get_collection(PublicIDCounter.COLLECTION).insert_one({'_id': collection, 'counter': docs_count})

        return docs_count

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update(self, collection: str, criteria: dict, data: dict, *args, add_to_set: bool = True, **kwargs):
        """
        Updates a document inside the given collection

        Args:
            collection (str): name of database collection
            criteria (dict): Filter to match document
            data: data to update

        Raises:
            DocumentUpdateError: When document could not be updated

        Returns:
            UpdateResult
        """
        try:
            formatted_data = {'$set': data} if add_to_set else data

            return self.get_collection(collection).update_one(criteria, formatted_data, *args, **kwargs)
        except Exception as err:
            LOGGER.debug("[update] Can't update document. Error: %s", err)
            raise DocumentUpdateError(collection, str(err)) from err


    def unset_update_many(self, collection: str, criteria: dict, data: str, *args, **kwargs):
        """
        Updates documents inside database

        Args:
            collection (str): name of database collection
            criteria (dict): filter of document
            data: data to delete

        Raises:
            DocumentUpdateError: When update has failed

        Returns:
            UpdateResult
        """
        try:
            formatted_data = {'$unset': {data: 1}}

            return self.get_collection(collection).update_many(criteria, formatted_data, *args, **kwargs)
        except Exception as err:
            LOGGER.debug("[unset_update_many] Can't update document. Error: %s", err)
            raise DocumentUpdateError(collection, str(err)) from err


    def update_many(self, collection: str, criteria: dict, update: dict, add_to_set:bool = False) -> UpdateResult:
        """update all documents that match the filter from a collection.

        Args:
            collection (str): Name of database collection
            criteria (dict): Filter that matches the documents to update
            update (dict): The modifications to apply
            add_to_set(bool): Add value to an array unless the value is already present

        Returns:
            A boolean acknowledged as true if the operation ran with write
            concern or false if write concern was disabled
        """
        try:
            formatted_data = {'$addToSet':update} if add_to_set else {'$set':update}

            return self.get_collection(collection).update_many(criteria, formatted_data)
        except Exception as err:
            LOGGER.debug("[update_many] Can't update document. Error: %s", err)
            raise DocumentUpdateError(collection, str(err)) from err


    def increment_public_id_counter(self, collection: str):
        """
        Increments the public_id counter for the given collection

        Args:
            collection (str): name of collection

        Raises:
            DocumentUpdateError: When counter could not be updated
        """
        working_collection = self.get_collection(PublicIDCounter.COLLECTION)

        query = {
            '_id': collection
        }

        counter_doc = working_collection.find_one(query)
        counter_doc['counter'] = counter_doc['counter'] + 1
        update_query = {'$set':{'counter':counter_doc['counter']}}

        try:
            self.get_collection(PublicIDCounter.COLLECTION).update_one(query, update_query)
        except Exception as err:
            LOGGER.debug("[increment_public_id_counter] Can't increment PublicID-Counter. Error: %s", err)
            raise DocumentUpdateError(collection, str(err)) from err


    def update_public_id_counter(self, collection: str, value: int):
        """
        Updates the public_id counter

        Args:
            collection (str): name of collection
            value (int): new value for counter

        Raises:
            DocumentUpdateError: When public_id counter could not be updated
        """
        try:
            working_collection = self.get_collection(PublicIDCounter.COLLECTION)

            query = {
                '_id': collection
            }

            counter_doc = working_collection.find_one(query)

            # init counter, if it was not found
            if counter_doc is None:
                self.__init_public_id_counter(collection)
                counter_doc = working_collection.find_one(query)

            # update counter only, if value is higher than counter
            if value > counter_doc['counter']:
                counter_doc['counter'] = value

                formatted_data = {'$set':counter_doc}

                self.get_collection(PublicIDCounter.COLLECTION).update_one(query, formatted_data)
        except Exception as err:
            LOGGER.debug("[update_public_id_counter] Can't increment PublicID-Counter. Error: %s", err)
            raise DocumentUpdateError(collection, str(err)) from err

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def find_all(self, collection, *args, **kwargs) -> list:
        """
        Retrives documents from the given collection

        Args:
            collection (str): name of collection
            *args: arguments for search operation
            **kwargs: key arguments

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            list: list of found documents
        """
        try:
            found_documents = self.find(collection, *args, **kwargs)

            return list(found_documents)
        except Exception as err:
            LOGGER.debug("[find_all] Can't retrive documents. Error: %s", err)
            raise DocumentGetError(collection, str(err)) from err


    def find(self, collection: str, *args, **kwargs):
        """
        General find function
        
        Args:
            collection (str): name of collection
            *args: arguments for search operation
            **kwargs: key arguments

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            Cursor with results
        """
        try:
            if 'projection' not in kwargs:
                kwargs.update({'projection': {'_id': 0}})

            return self.get_collection(collection).find(*args, **kwargs)
        except Exception as err:
            LOGGER.debug("[find] Can't retrive documents. Error: %s", err)
            raise DocumentGetError(collection, str(err)) from err


    def find_one_by(self, collection: str, *args, **kwargs) -> dict:
        """
        Find one specific document by special requirements

        Args:
            collection (str): name of database collection

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            found document
        """
        try:
            cursor_result = self.find(collection, limit=1, *args, **kwargs)
        except Exception as err:
            LOGGER.debug("[find_one_by] Can't retrive document. Error: %s", err)
            raise DocumentGetError(collection, str(err)) from err

        for result in cursor_result.limit(-1):
            return result

        raise NoDocumentFound(collection)


    def find_one(self, collection: str, public_id: int, *args, **kwargs):
        """
        Retrieves a single document with the given public_id from the given collection 

        Args:
            collection (str): name of database collection
            public_id (int): public_id of document

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            document with given public_id
        """
        try:
            cursor_result = self.find(collection, {'public_id': public_id}, limit=1, *args, **kwargs)

            for result in cursor_result.limit(-1):
                return result
        except Exception as err:
            LOGGER.debug("[find_one] Can't retrive document. Error: %s", err)
            raise DocumentGetError(collection, str(err)) from err

    def count(self, collection: str, filter: dict = None, *args, **kwargs):
        """
        Count documents based on filter parameters

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

        Raises:
            DocumentAggregationError: When the aggregate operation fails

        Returns:
            returns computed results
        """
        try:
            return self.get_collection(collection).aggregate(*args, **kwargs, allowDiskUse=True)
        except Exception as err:
            LOGGER.debug("[aggregate] Aggregation failed. Error: %s", err)
            raise DocumentAggregationError(str(err)) from err


    def get_highest_id(self, collection: str) -> int:
        """wrapper function
        calls get_document_with_highest_id() and returns the public_id

        Args:
            collection (str): name of database collection

        Raises:
            DocumentGetError: When documents could not be retrieved

        Returns:
            int: highest public id
        """
        try:
            try:
                formatted_sort = [('public_id', -1)]

                highest_id = self.find_one_by(collection=collection, sort=formatted_sort)

                highest = int(highest_id['public_id'])
            except NoDocumentFound:
                return 0

            return highest
        except Exception as err:
            LOGGER.debug("[get_highest_id] Can't retrive document. Error: %s", err)
            raise DocumentGetError(collection, str(err)) from err


    def get_next_public_id(self, collection: str) -> int:
        """TODO: document"""
        try:
            found_counter = self.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})
            new_id = found_counter['counter'] + 1
        except (NoDocumentFound, Exception):
            docs_count = self.__init_public_id_counter(collection)
            new_id = docs_count + 1
        finally:
            self.increment_public_id_counter(collection)

        return new_id

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete(self, collection: str, criteria: dict) -> DeleteResult:
        """delete document inside database

        Args:
            collection (str): name of database collection
            filter (dict): filter query

        Raises:
            DocumentDeleteError: When documents could not be deleted

        Returns:
            acknowledged
        """
        try:
            return self.get_collection(collection).delete_one(criteria)
        except Exception as err:
            LOGGER.debug("[delete] Can't delete document. Error: %s", err)
            raise DocumentDeleteError(collection, str(err)) from err


    def delete_many(self, collection: str, **requirements: dict) -> DeleteResult:
        """
        Removes all documents that match the filter from a collection

        Args:
            collection (str): name of database collection
            filter (dict): Specifies deletion criteria using query operators.

        Raises:
            DocumentDeleteError: When documents could not be deleted

        Returns:
            A boolean acknowledged as true if the operation ran
            with write concern or false if write concern was disabled
        """
        try:
            requirements_filter = {}
            for k, req in requirements.items():
                requirements_filter.update({k: req})

            return self.get_collection(collection).delete_many(requirements_filter)
        except Exception as err:
            LOGGER.debug("[delete_many] Can't delete documents. Error: %s", err)
            raise DocumentDeleteError(collection, str(err)) from err

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
                self.__init_public_id_counter(collection)

            status = self.insert(collection, self.get_root_location_data())
        else:
            status = self.update(collection,{'public_id':1},self.get_root_location_data())

        return status

# ------------------------------------------- CmdbSectionTemplate - Section ------------------------------------------ #

    def init_predefined_templates(self, collection: str):
        """
        Checks if all predefined templates are created, else create them
        """
        ## check if counter is created in db, else create one
        counter = self.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})

        if not counter:
            self.__init_public_id_counter(collection)

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


    def create_general_report_category(self, collection: str):
        """
        Creates the General Report Category
        """
        ## check if counter is created in db, else create one
        counter = self.get_collection(PublicIDCounter.COLLECTION).find_one(filter={'_id': collection})

        if not counter:
            self.__init_public_id_counter(collection)

        result = self.get_collection(collection).find_one(filter={'name': 'General'})

        if not result:
            # The template does not exist, create it
            LOGGER.info("Creating 'General' Report Category")

            general_category = {
                'name': 'General',
                'predefined': True,
            }

            self.insert(collection, general_category)
