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
Manages Objects in the backend
"""
import logging
import json
from queue import Queue
from typing import Union
from bson import Regex, json_util

from cmdb.database.mongo_database_manager import MongoDatabaseManager
from cmdb.manager.base_manager import BaseManager

from cmdb.event_management.event import Event
from cmdb.cmdb_objects.cmdb_object import CmdbObject
from cmdb.manager.query_builder.builder import Builder
from cmdb.manager.query_builder.builder_parameters import BuilderParameters
from cmdb.user_management.models.user import UserModel
from cmdb.security.acl.helpers import verify_access
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.framework.models.type import TypeModel
from cmdb.database.utils import object_hook
from cmdb.framework.results import IterationResult

from cmdb.errors.manager.object_manager import ObjectManagerGetError,\
                                               ObjectManagerInitError,\
                                               ObjectManagerInsertError,\
                                               ObjectManagerDeleteError
from cmdb.errors.manager import ManagerGetError, ManagerInsertError, ManagerIterationError, ManagerUpdateError
from cmdb.errors.security import AccessDeniedError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                ObjectsManager - CLASS                                                #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectsManager(BaseManager):
    """
    Interface for objects between backend and database
    Extends: BaseMaanger
    """
    def __init__(self, dbm: MongoDatabaseManager, event_queue: Union[Queue, Event] = None, database:str = None):
        """
        Set the database connection and the queue for sending events

        Args:
            dbm (MongoDatabaseManager): Database connection
            event_queue (Queue, Event): The queue for events in RabbitMQ
            database (str): name of database for cloud mode
        """
        self.event_queue = event_queue

        if database:
            dbm.connector.set_database(database)

        super().__init__(CmdbObject.COLLECTION, dbm)

# --------------------------------------------------- CRUD - CREATE -------------------------------------------------- #

    def insert_object(self,
                      data: dict,
                      user: UserModel = None,
                      permission: AccessControlPermission = None) -> int:
        """
        Insert new Object

        Args:
            data: Object data
            user: User requesting the action
            permission: Extended user acl rights

        Raises:
            ObjectManagerInsertError: If an error occured during inserting the object
        Returns:
            Public ID of the new object in database
        """
        new_object = None

        try:
            new_object = CmdbObject(**data)
        except Exception as err:
            LOGGER.debug("[insert_object] Error while initialising object. Error: %s", str(err))
            raise ObjectManagerInitError(str(err)) from err

        try:
            object_type = self.get_object_type(new_object.type_id)
        except ObjectManagerGetError as err:
            raise ObjectManagerGetError(err) from err

        if not object_type.active:
            raise AccessDeniedError(f'Objects cannot be created because type `{object_type.name}` is deactivated.')

        verify_access(object_type, user, permission)

        try:
            ack = self.insert(new_object.__dict__)
        except ManagerInsertError as err:
            LOGGER.debug("[insert_object] Error while inserting object. Error: %s", str(err))
            raise ObjectManagerInsertError(err) from err
        except Exception as err:
            #ERROR-FIX
            LOGGER.debug("[insert_object] Error while inserting object. Exception: %s", str(err))
            raise ObjectManagerInsertError(err) from err

        try:
            if self.event_queue:
                event = Event("cmdb.core.object.added",
                                {
                                    "id": new_object.get_public_id(),
                                    "type_id": new_object.get_type_id(),
                                    "user_id": new_object.author_id,
                                    "event": 'insert'
                                }
                             )

                self.event_queue.put(event)
        except Exception:
            #ERROR-FIX
            LOGGER.debug("[insert_object] Error while creating object event. Error: %s", str(err))

        return ack

# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get_object(self, public_id: int,
            user: UserModel = None,
            permission: AccessControlPermission = None) -> CmdbObject:
        """
        Get a single object by its id

        Args:
            public_id (int): ID of the object
            user: Request user
            permission: ACL permission

        Raises:
            ObjectManagerGetError: If object was not found

        Returns:
            (CmdbObject): Requested object
        """
        try:
            requested_object = self.get_one(public_id)
        except Exception as err:
            LOGGER.debug("[get_object] Error: %s, Type: %s", err, type(err))
            raise ObjectManagerGetError(f"Error while retrieving object with ID: {public_id}! Error: {err}") from err

        if requested_object:
            requested_object = CmdbObject.from_data(requested_object)
            object_type = self.get_object_type(requested_object.type_id)
            verify_access(object_type, user, permission)

            return requested_object

        raise ObjectManagerGetError(f'Object with ID: {public_id} not found!')


    def iterate(self,
                builder_params: BuilderParameters,
                user: UserModel = None,
                permission: AccessControlPermission = None) -> IterationResult[CmdbObject]:
        """
        TODO: document
        """
        try:
            aggregation_result, total = self.iterate_query(builder_params, user, permission)

            iteration_result: IterationResult[CmdbObject] = IterationResult(aggregation_result, total)
            iteration_result.convert_to(CmdbObject)
        #ERROR-FIX
        except Exception as err:
            raise ManagerIterationError(err) from err

        return iteration_result


    def get_objects_by(self,
                       sort='public_id',
                       direction=-1,
                       user: UserModel = None,
                       permission: AccessControlPermission = None,
                       **requirements):
        """TODO: document"""
        ack = []

        objects = self.get_many(sort=sort, direction=direction, **requirements)

        for obj in objects:
            cur_object = CmdbObject(**obj)

            try:
                #ERROR-FIX (Separate try-except bloc for get_object_type())
                cur_type = self.get_object_type(cur_object.type_id)
                verify_access(cur_type, user, permission)
            except Exception:
                #ERROR-FIX (Raise kinda AccesDeniedError)
                continue

            ack.append(CmdbObject(**obj))

        return ack


    def group_objects_by_value(self,
                               value: str,
                               match=None,
                               user: UserModel = None,
                               permission: AccessControlPermission = None):
        """This method does not actually
           performs the find() operation
           but instead returns
           a objects grouped by type of the documents that meet the selection criteria.

           Args:
               value (str): grouped by value
               match (dict): stage filters the documents to only pass documents.
               user (UserModel): request user
               permission (AccessControlPermission):  ACL operations
           Returns:
               returns the objects grouped by value of the documents
           """
        ack = []
        agr = []

        if match:
            agr.append({'$match': match})

        agr.append({
            '$group': {
                '_id': '$' + value,
                'result': {'$first': '$$ROOT'},
                'count': {'$sum': 1},
            }
        })

        agr.append({'$sort': {'count': -1}})

        objects = self.aggregate_objects(agr)

        for obj in objects:
            cur_object = CmdbObject(**obj['result'])
            try:
                cur_type = self.get_object_type(cur_object.type_id)
                verify_access(cur_type, user, permission)
            except Exception:
                #ERROR-FIX
                continue

            ack.append(obj)

        return ack


    def get_object_type(self, type_id: int) -> TypeModel:
        """
        Retrieves the CmdbType for the given public_id of the CmdbType

        Args:
            type_id (int): public_id of the CmdbType

        Raises:
            ObjectManagerGetError: When CmdbType could not be retrieved

        Returns:
            TypeModel: CmdbType with the given type_id
        """
        try:
            requested_type = self.get_one_from_other_collection(TypeModel.COLLECTION, type_id)
            requested_type = TypeModel.from_data(requested_type)
        except Exception as err:
            LOGGER.debug("[get_object_type] Error: %s, Type: %s", err, type(err))
            raise ObjectManagerGetError(f"Error while retrieving type with ID: {type_id}. Error: {err}") from err

        return requested_type


    def count_objects(self, criteria: dict = None):
        """
        Returns the number of objects with the given criteria

        Args:
            criteria (dict): Filter for counting documents like {'type_id: 1} 

        Raises:
            ObjectManagerGetError: When an error occures during counting objects

        Returns:
            (int): Returns the number of documents with the given criteria
        """
        try:
            if criteria:
                object_count = self.count_documents(self.collection, filter=criteria)
            else:
                object_count = self.count_documents(self.collection)
        except ManagerGetError as err:
            raise ObjectManagerGetError(err) from err

        return object_count


    def get_new_object_public_id(self) -> int:
        """
        Gets the next couter for the public_id from database and increases it

        Returns:
            int: The next public_id for CmdbObject
        """
        return self.get_next_public_id()


    def aggregate_objects(self, pipeline: list[dict], **kwargs):
        """TODO: document"""
        try:
            return self.aggregate(pipeline=pipeline, **kwargs)
        except Exception as error:
            raise ObjectManagerGetError(error) from error


    def get_mds_references_for_object(self, referenced_object: CmdbObject, query_filter: Union[dict, list]):
        """TODO: document"""
        object_type_id = referenced_object.type_id

        query = []

        if isinstance(query_filter, dict):
            query.append(query_filter)
        elif isinstance(query_filter, list):
            for a_filter in query_filter:
                if "$match" in a_filter and len(a_filter["$match"]) > 0:
                    if "type_id" in a_filter["$match"]:
                        filter_type_id = a_filter["$match"]["type_id"]
                        del a_filter["$match"]["type_id"]
                        a_filter["$match"]["public_id"] = filter_type_id

            query += query_filter

        # Get all types which reference this type
        query.append({'$match': {"$and": [
                                    {"fields.type": "ref"},
                                    {"fields.ref_types": object_type_id}
                                ]}
                    })

        # Filter the public_id's of these types
        query.append({'$project': {"public_id": 1, "_id": 0}})

        # Get all objects of these types
        query.append(Builder.lookup_(_from='framework.objects',
                                     _local='public_id',
                                     _foreign='type_id',
                                     _as='type_objects'))

        # Filter out types which don't have any objects
        query.append({'$match': {"type_objects.0": {"$exists": True}}})

        # Spread out the arrays
        query.append(Builder.unwind_({'path': '$type_objects'}))

        # Filter the objects which actually have any multi section data
        query.append({'$match': {"type_objects.multi_data_sections.0": {"$exists": True}}})

        # Remove the public_id field
        query.append({'$project': {"type_objects": 1}})

        # Spread out as a list
        query.append({'$replaceRoot': {"newRoot": '$type_objects'}})

        query.append({'$project': {"_id": 0}})

        # query.append({'$sort': {sort: order}})

        try:
            results = list(self.aggregate_from_other_collection(TypeModel.COLLECTION, query))
        except ManagerIterationError as err:
            #ERROR-FIX
            LOGGER.debug("[get_mds_references_for_object] aggregation error: %s", err.message)

        matching_results = []

        # Check if the mds data references the current object
        for result in results:
            try:
                for mds_entry in result["multi_data_sections"]:
                    for value in mds_entry["values"]:
                        data_set: dict
                        for data_set in value["data"]:
                            if self.__is_ref_field(data_set["name"], result) and \
                            "value" in data_set.keys() and \
                            data_set["value"] == referenced_object.public_id:
                                matching_results.append(result)
                                # this result is a match => go back to outer loop
                                raise StopIteration()
            except StopIteration:
                pass

        return matching_results


    #REFACTOR-FIX
    def references(self,
                   object_: CmdbObject,
                   criteria: dict,
                   limit: int,
                   skip: int,
                   sort: str,
                   order: int,
                   user: UserModel = None,
                   permission: AccessControlPermission = None) -> IterationResult[CmdbObject]:
        """TODO: document"""
        query = []

        #ERROR-FIX (it is only one of these)
        if isinstance(criteria, dict):
            query.append(criteria)
        elif isinstance(criteria, list):
            query += criteria

        query.append(Builder.lookup_(_from='framework.types', _local='type_id', _foreign='public_id', _as='type'))

        query.append(Builder.unwind_({'path': '$type'}))

        field_ref_query = {
                'type.fields.type': 'ref',
                '$or': [
                    {'type.fields.ref_types': Regex(f'.*{object_.type_id}.*', 'i')},
                    {'type.fields.ref_types': object_.type_id}
                ]
        }

        section_ref_query = {
                'type.render_meta.sections.type': 'ref-section',
                'type.render_meta.sections.reference.type_id': object_.type_id
        }

        query.append(Builder.match_(Builder.or_([field_ref_query, section_ref_query])))
        query.append(Builder.match_({'fields.value': object_.public_id}))

        builder_params = BuilderParameters(criteria=query, sort=sort, order=order)

        # limit and skip will be handled when merged with the MDS results in '__merge_mds_references()'
        result = self.iterate(builder_params, user, permission)
        mds_result = self.get_mds_references_for_object(object_, criteria)

        merge_result = self.__merge_mds_references(mds_result, result, limit, skip, sort, order)

        return merge_result

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update_object(self,
                      public_id: int,
                      data: Union[CmdbObject, dict],
                      user: UserModel = None,
                      permission: AccessControlPermission = None):
        """
        Update a existing type in the system.
        Args:
            public_id (int): PublicID of the type in the system.
            data: New object data
            user: Request user
            permission: ACL permission

        Notes:
            If a CmdbObject instance was passed as data argument, \
            it will be auto converted via the model `to_json` method.
        """

        if isinstance(data, CmdbObject):
            instance = CmdbObject.to_json(data)
        else:
            instance = json.loads(json.dumps(data, default=json_util.default), object_hook=object_hook)

        object_type = self.get_object_type(instance.get('type_id'))

        if not object_type.active:
            #ERROR-FIX
            raise AccessDeniedError(f'Objects cannot be updated because type `{object_type.name}` is deactivated.')
        verify_access(object_type, user, permission)

        update_result = self.update(criteria={'public_id': public_id}, data=instance)

        #ERROR-FIX
        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')

        if self.event_queue and user:
            try:
                event = Event("cmdb.core.object.updated",
                            {
                                "id": public_id,
                                "type_id": instance.get('type_id'),
                                "user_id": user.get_public_id(),
                                'event': 'update'
                                })
                self.event_queue.put(event)
            except Exception as err:
                LOGGER.debug("[update_object] Event error: %s, Type: %s", err, type(err))

        return update_result


    def update_many_objects(self, query: dict, update: dict, add_to_set: bool = False):
        """
        update all documents that match the filter from a collection.
        Args:
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            acknowledgment of database
        """
        try:
            update_result = self.update_many(criteria=query, update=update, add_to_set=add_to_set)
        except (ManagerUpdateError, AccessDeniedError) as err:
            #ERROR-FIX
            raise err

        return update_result

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_object(self, public_id: int, user: UserModel, permission: AccessControlPermission = None):
        """TODO: document"""
        try:
            type_id = self.get_object(public_id).type_id
        except ObjectManagerGetError as err:
            raise ObjectManagerDeleteError(str(err)) from err

        try:
            object_type = self.get_object_type(type_id)
        except ObjectManagerGetError as err:
            raise ObjectManagerDeleteError(str(err)) from err

        if not object_type.active:
            #ERROR-FIX
            raise AccessDeniedError(f'Objects cannot be removed because type `{object_type.name}` is deactivated.')

        verify_access(object_type, user, permission)

        #ERROR-FIX (SWAP WITH DELETEION IN WORKFLOW)
        try:
            if self.event_queue:
                event = Event("cmdb.core.object.deleted",
                              {"id": public_id,
                               "type_id": type_id,
                               "user_id": user.get_public_id(),
                               "event": 'delete'})
                self.event_queue.put(event)
        except Exception as err:
            #ERROR-FIX
            raise ObjectManagerDeleteError(str(err)) from err

        try:
            ack = self.delete({'public_id': public_id})
            return ack
        except Exception as err:
            raise ObjectManagerDeleteError(str(err)) from err


    def delete_many_objects(self, filter_query: dict, public_ids, user: UserModel):
        """TODO: document"""
        try:
            ack = self.delete_many(filter_query)
        except Exception as err:
            raise ObjectManagerDeleteError(str(err)) from err

        try:
            if self.event_queue:
                event = Event("cmdb.core.objects.deleted", {"ids": public_ids,
                                                            "user_id": user.get_public_id(),
                                                            "event": 'delete'})
                self.event_queue.put(event)
        except Exception as err:
            LOGGER.debug("[delete_many_objects] event_queue Error: %s , Type: %s", err , type(err))

        return ack


    def delete_all_object_references(self, public_id: int):
        """
        Delete all references to the object with the given public_id

        Args:
            public_id (int): public_id of targeted object
        """
        object_instance: CmdbObject = self.get_object(public_id)
        # Get all objects which reference the targeted object
        iteration_result: IterationResult = self.references(
                                                    object_=object_instance,
                                                    criteria={'$match': {'active': {'$eq': True}}},
                                                    limit=0,
                                                    skip=0,
                                                    sort='public_id',
                                                    order=1
                                                )

        referenced_objects: list[dict] =  [object_.__dict__ for object_ in iteration_result.results]

        # Delete the reference in each object and update them
        for refed_object in referenced_objects:
            for field in refed_object['fields']:
                field_value: int = field['value']
                field_name: str = field['name']

                if field_name.startswith('ref-') and field_value == public_id:
                    field['value'] = ""

            refed_object_id = refed_object['public_id']
            self.update_object(refed_object_id, refed_object)

# ------------------------------------------------- HELPER FUNCTIONS ------------------------------------------------- #

    def __merge_mds_references(self,
                                mds_result: list,
                                obj_result: IterationResult,
                                limit: int,
                                skip: int,
                                sort: str,
                                order: int):
        """TODO: document"""
        try:
            referenced_ids = []

            # get public_id's of all currently referenced objects
            for obj in obj_result.results:
                referenced_ids.append(obj.public_id)


            # add mds objects to normal references if they are not already inside
            for ref_object in mds_result:
                tmp_object = CmdbObject.from_data(ref_object)

                if tmp_object.public_id not in referenced_ids:
                    obj_result.results.append(tmp_object)

            obj_result.total = len(obj_result.results)

            # sort all findings according to sort and order
            descending_order = order == -1
            try:
                obj_result.results.sort(key=lambda x: getattr(x, sort), reverse=descending_order)
            except Exception as err:
                #ERROR-FIX
                LOGGER.debug("References sorting error: %s", err)

            # just keep the given limit of objects if limit > 0
            if limit > 0:
                list_length = limit + skip

                # if the list_length is longer than the object_list then just set it to len(object_list)
                list_length = min(list_length, len(obj_result.results))

                try:
                    obj_result.results = obj_result.results[skip:list_length]
                except Exception as err:
                    #ERROR-FIX
                    LOGGER.debug("References list slice error: %s", err)

            # obj_result.total = len(obj_result.results)
        except Exception as err:
            #ERROR-FIX
            LOGGER.info("[__merge_mds_references] Error: %s", err)

        return obj_result


    def __is_ref_field(self, field_name: str, ref_object: dict) -> bool:
        """TODO: document"""
        ref_type = self.get_object_type(ref_object["type_id"])

        for field in ref_type.fields:
            if field["name"] == field_name and field["type"] == "ref":
                return True

        return False
