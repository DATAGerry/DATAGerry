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
TODO: document
"""
import json
import logging
from typing import Union
from bson import json_util

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.framework import TypeModel
from cmdb.database.utils import object_hook
from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.framework.models.type_model.type_field_section import TypeFieldSection
from cmdb.manager.query_builder.base_query_builder import BaseQueryBuilder
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.framework.results import IterationResult
from cmdb.framework.results.list import ListResult

from cmdb.errors.manager import ManagerUpdateError,\
                                ManagerDeleteError,\
                                ManagerGetError,\
                                ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                 TypesManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class TypesManager(BaseManager):
    """
    Manager for the type module. Manages the CRUD functions of the types and the iteration over the collection.
    Extends: BaseManager
    Depends: ObjectsManager
    """
    def __init__(self, dbm: MongoDatabaseManager, database: str = None):
        if database:
            dbm.connector.set_database(database)

        self.query_builder = BaseQueryBuilder()

        self.objects_manager = ObjectsManager(dbm)

        super().__init__(TypeModel.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_type(self, new_type: Union[TypeModel, dict]) -> int:
        """
        Insert a single type into the system.

        Args:
            type (dict): Raw data of the type.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted type
        """
        if isinstance(new_type, TypeModel):
            type_to_add = TypeModel.to_json(new_type)
        else:
            type_to_add = json.loads(json.dumps(new_type, default=json_util.default), object_hook=object_hook)

        #TODO: ERROR-FIX (Add try/except block)
        return self.insert(type_to_add)

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_new_type_public_id(self) -> int:
        """
        Gets the next couter for the public_id from database and increases it

        Returns:
            int: The next public_id for CmdbType
        """
        return self.get_next_public_id()


    def get_type(self, public_id: int) -> TypeModel:
        """
        Get a single type by its id.

        Args:
            public_id (int): ID of the type.

        Returns:
            TypeModel: Instance of TypeModel with data.
        """
        requested_type = self.get_one(public_id)

        try:
            return TypeModel.from_data(requested_type)
        except Exception as err:
            #TODO: ERROR-FIX (Needs a TypesManagerGetError)
            raise ManagerGetError(str(err)) from err


    def iterate(self, builder_params: BuilderParameters) -> IterationResult[TypeModel]:
        """
        Iterate over a collection of type resources.

        Args:
            filter: match requirements of field values
            limit: max number of elements to return
            skip: number of elements to skip first
            sort: sort field
            order: sort order

        Returns:
            IterationResult: Instance of IterationResult with generic TypeModel.
        """

        try:
            query: list[dict] = self.query_builder.build(builder_params)
            count_query: list[dict] = self.query_builder.count(builder_params.get_criteria())

            aggregation_result = list(self.aggregate(query))
            total_cursor = self.aggregate(count_query)

            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            #TODO: ERROR-FIX
            raise ManagerIterationError(err) from err

        iteration_result: IterationResult[TypeModel] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(TypeModel)

        return iteration_result


    def find_types(self, criteria: dict) -> ListResult[TypeModel]:
        """
        Get a list of types by a filter query.
        Args:
            filter: Filter for matched querys

        Returns:
            ListResult
        """
        results = self.find(criteria=criteria)
        types: list[TypeModel] = [TypeModel.from_data(result) for result in results]

        return ListResult(types)


    def count_types(self):
        """TODO: document"""
        return self.count_documents(TypeModel.COLLECTION)


        # TODO: REFACTOR-FIX (Move to TypeManager once refactored)
    def get_all_types(self) -> list[TypeModel]:
        """TODO: document"""
        try:
            raw_types: list[dict] = self.get_many()
        except Exception as err:
            raise ManagerGetError(err) from err
        try:
            return [TypeModel.from_data(type) for type in raw_types]
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerGetError(err) from err


    def get_types_by(self, sort='public_id', **requirements):
        """TODO: document"""
        try:
            return [TypeModel.from_data(data) for data in self.get_many(sort=sort, **requirements)]
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerGetError(err) from err


    def get_type_aggregate(self, arguments):
        """This method does not actually
           performs the find() operation
           but instead returns
           a objects sorted by value of the documents that meet the selection criteria.

           Args:
               arguments: query search for
           Returns:
               returns the list of CMDB Types sorted by value of the documents
           """
        type_list = []
        cursor = self.dbm.aggregate(TypeModel.COLLECTION, arguments)

        for document in cursor:
            put_data = json.loads(json_util.dumps(document), object_hook=object_hook)
            type_list.append(TypeModel.from_data(put_data))

        return type_list

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_type(self, public_id: int, update_type: Union[TypeModel, dict]):
        """
        Update a existing type in the system.
        Args:
            public_id (int): PublicID of the type in the system.
            type: New type data

        Notes:
            If a TypeModel instance was passed as type argument, \
            it will be auto converted via the model `to_json` method.
        """
        if isinstance(update_type, TypeModel):
            new_version_type = TypeModel.to_json(update_type)
        else:
            new_version_type = json.loads(json.dumps(update_type, default=json_util.default), object_hook=object_hook)

        update_result = self.update(criteria={'public_id': public_id}, data=new_version_type)

        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')

        return update_result

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_type(self, public_id: int) -> TypeModel:
        """
        Delete a existing type by its PublicID.

        Args:
            public_id (int): PublicID of the type in the system.

        Returns:
            TypeModel: The deleted type as its model.
        """
        raw_type: TypeModel = self.get_type(public_id)
        try:
            self.delete({'public_id': public_id})
        except Exception as err:
            #TODO: ERROR-FIX
            raise ManagerDeleteError(str(err)) from err

        return raw_type

# -------------------------------------------------- HELPER METHODS -------------------------------------------------- #

    def fields_diff(self, initial_fields: list, new_fields: list,  check_added: bool = False) -> list:
        """TODO: document"""
        if check_added:
            # check which fields were added
            return [field_name for field_name in new_fields if field_name not in initial_fields]

        #check which fields were deleted
        return [field_name for field_name in initial_fields if field_name not in new_fields]


    def create_mds_field_entries(self, fields_to_add: list, data_set) -> list:
        """TODO: document"""
        try:
            for field_name in fields_to_add:

                new_field = {
                    "name": field_name,
                    "value": None
                }

                data_set["data"].append(new_field)
        except Exception as err:
            #TODO- ERROR-FIX
            LOGGER.debug("Error in create_mds_field_entries(): %s", err)

        return data_set


    def delete_mds_field_entries(self, fields_to_delete: list, data_set: list) -> list:
        """TODO: document"""
        to_delete = []

        try:
            # get all fields which should be deleted
            for field_name in fields_to_delete:
                index: int = 0

                for entry in data_set["data"]:
                    if entry["name"] == field_name:
                        break

                    index += 1

                to_delete.append(index)

            # delete from end
            for idx in to_delete[::-1]:
                del data_set["data"][idx]

        except Exception as err:
            #TODO: ERROR-FIX
            LOGGER.debug("Error in delete_mds_field_entries(): %s", err) 

        return data_set


    def update_multi_data_fields(self, target_type: TypeModel, added_fields: dict, deleted_fields: dict):
        """TODO: document"""
        # get all objects of this type
        #TODO: REFACTOR-FIX (remove dependency on ObjectsManager)
        all_type_objects = self.objects_manager.get_objects_by(type_id=target_type.public_id)

        # update the multi-data-sections
        an_object: CmdbObject
        for an_object in all_type_objects:
            try:
                for current_mds_section in an_object.multi_data_sections:
                    section_id = current_mds_section["section_id"]
                    fields_to_add = added_fields[section_id]
                    fields_to_delete = deleted_fields[section_id]

                    # add new fields and remove deleted fields
                    if len(fields_to_add) > 0:
                        for data_set in current_mds_section["values"]:
                            data_set = self.create_mds_field_entries(fields_to_add, data_set)

                    if len(fields_to_delete) > 0:
                        for data_set in current_mds_section["values"]:
                            data_set = self.delete_mds_field_entries(fields_to_delete, data_set)

            except Exception as err:
                LOGGER.error("Error while updating multi data fields of objects: %s", err)

        return all_type_objects


    def handle_mutli_data_sections(self, target_type: TypeModel, updated_data: dict):
        """TODO: document"""
        added_fields: dict = {}
        deleted_fields: dict = {}

        a_section: TypeFieldSection
        for a_section in target_type.render_meta.sections:
            # LOGGER.info(f"a type section: {a_section}")

            if a_section.type == "multi-data-section":
                for updated_section in updated_data["render_meta"]["sections"]:
                    # LOGGER.info(f"new sections: {updated_section}")

                    if a_section.type == updated_section["type"] and a_section.name == updated_section["name"]:
                        # get the field changes for each multi-data-section
                        added_fields[a_section.name] = self.fields_diff(a_section.fields,
                                                                        updated_section["fields"],
                                                                        True)
                        deleted_fields[a_section.name] = self.fields_diff(a_section.fields,
                                                                          updated_section["fields"],
                                                                          False)

        return self.update_multi_data_fields(target_type, added_fields, deleted_fields)
