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

from cmdb.database.utils import object_hook
from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.framework import TypeModel
from cmdb.framework.models.type_model.type_field_section import TypeFieldSection
from cmdb.manager.managers import ManagerBase
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.results.list import ListResult
from cmdb.framework.utils import PublicID
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerUpdateError, ManagerDeleteError
from cmdb.search import Pipeline
from cmdb.framework.cmdb_object import CmdbObject

import cmdb.framework.cmdb_object_manager as com

# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  TypeManager - CLASS                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
class TypeManager(ManagerBase):
    """
    Manager for the type module. Manages the CRUD functions of the types and the iteration over the collection.
    """

    def __init__(self, database_manager: DatabaseManagerMongo, database: str = None):
        """
        Constructor of `TypeManager`

        Args:
            database_manager: Connection to the database class.
        """
        if database:
            database_manager.connector.set_database(database)

        super().__init__(TypeModel.COLLECTION, database_manager=database_manager)


    def iterate(self, filter: dict, limit: int, skip: int, sort: str, order: int, *args, **kwargs) \
            -> IterationResult[TypeModel]:
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
            query: Pipeline = self.builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)
            count_query: Pipeline = self.builder.count(filter=filter)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        iteration_result: IterationResult[TypeModel] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(TypeModel)
        return iteration_result


    def find(self, filter: dict, *args, **kwargs) -> ListResult[TypeModel]:
        """
        Get a list of types by a filter query.
        Args:
            filter: Filter for matched querys

        Returns:
            ListResult
        """
        results = self._get(self.collection, filter=filter)
        types: list[TypeModel] = [TypeModel.from_data(result) for result in results]
        return ListResult(types)


    def get(self, public_id: Union[PublicID, int]) -> TypeModel:
        """
        Get a single type by its id.

        Args:
            public_id (int): ID of the type.

        Returns:
            TypeModel: Instance of TypeModel with data.
        """
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in cursor_result.limit(-1):
            return TypeModel.from_data(resource_result)
        raise ManagerGetError(f'Type with ID: {public_id} not found!')


    def insert(self, type: Union[TypeModel, dict]) -> PublicID:
        """
        Insert a single type into the system.

        Args:
            type (dict): Raw data of the type.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted type
        """
        if isinstance(type, TypeModel):
            type = TypeModel.to_json(type)
        elif isinstance(type, dict):
            type = json.loads(json.dumps(type, default=json_util.default), object_hook=object_hook)

        return self._insert(self.collection, resource=type)


    def update(self, public_id: Union[PublicID, int], type: Union[TypeModel, dict]):
        """
        Update a existing type in the system.
        Args:
            public_id (int): PublicID of the type in the system.
            type: New type data

        Notes:
            If a TypeModel instance was passed as type argument, \
            it will be auto converted via the model `to_json` method.
        """
        if isinstance(type, TypeModel):
            type = TypeModel.to_json(type)
        elif isinstance(type, dict):
            type = json.loads(json.dumps(type, default=json_util.default), object_hook=object_hook)

        update_result = self._update(self.collection, filter={'public_id': public_id}, resource=type)
        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')

        return update_result


    def delete(self, public_id: Union[PublicID, int]) -> TypeModel:
        """
        Delete a existing type by its PublicID.

        Args:
            public_id (int): PublicID of the type in the system.

        Returns:
            TypeModel: The deleted type as its model.
        """
        raw_type: TypeModel = self.get(public_id=public_id)
        delete_result = self._delete(self.collection, filter={'public_id': public_id})
        if delete_result.deleted_count == 0:
            raise ManagerDeleteError(err='No type matched this public id')
        return raw_type

# -------------------------------------------------- HELPER SECTION -------------------------------------------------- #

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


    def update_multi_data_fields(self, target_type: TypeModel, added_fields: dict, deleted_fields: dict):
        """TODO: document"""
        # get all objects of this type
        cmdb_object_manager = com.CmdbObjectManager(self._database_manager)
        all_type_objects = cmdb_object_manager.get_objects_by_type(target_type.public_id)

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
                LOGGER.error(f"Error while updating multi data fields of objects: {err}")

        return all_type_objects



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
            LOGGER.debug(f"Error in create_mds_field_entries(): {err}")

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
            LOGGER.debug(f"Error in delete_mds_field_entries(): {err}") 

        return data_set


    def fields_diff(self, initial_fields: list, new_fields: list,  check_added: bool = False) -> list:
        """TODO: document"""
        if check_added:
            # check which fields were added
            return [field_name for field_name in new_fields if field_name not in initial_fields]

        #check which fields were deleted
        return [field_name for field_name in initial_fields if field_name not in new_fields]
