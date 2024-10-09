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
Manages Objects in Datagerry
"""
import json
import logging
from queue import Queue
from typing import Union
from bson import Regex, json_util

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.manager.managers import ManagerQueryBuilder, ManagerBase
from cmdb.manager.objects_manager import ObjectsManager

from cmdb.database.utils import object_hook
from cmdb.event_management.event import Event
from cmdb.framework import CmdbObject
from cmdb.security.acl.helpers import verify_access
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.search import Query, Pipeline
from cmdb.manager.query_builder.builder import Builder
from cmdb.security.acl.builder import AccessControlQueryBuilder
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management.models.user import UserModel
from cmdb.framework import TypeModel

from cmdb.errors.security import AccessDeniedError
from cmdb.errors.manager import ManagerUpdateError, ManagerGetError, ManagerIterationError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  ObjectQueryBuilder                                                  #
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectQueryBuilder(ManagerQueryBuilder):
    """
    Extends: ManagerQueryBuilder
    """
    def __init__(self):
        super().__init__()


    def build(self, filter: Union[list[dict], dict], limit: int, skip: int, sort: str, order: int,
              user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) -> \
            Union[Query, Pipeline]:
        """
        Converts the parameters from the call to a mongodb aggregation pipeline
        Args:
            filter: dict or list of dict query/queries which the elements have to match.
            limit: max number of documents to return.
            skip: number of documents to skip first.
            sort: sort field
            order: sort order
            user: request user
            permission: AccessControlPermission
            *args:
            **kwargs:

        Returns:
            The `FrameworkQueryBuilder` query pipeline with the parameter contents.
        """
        self.clear()
        loading_dep_preset = [
            self.lookup_(_from='framework.types', _local='type_id', _foreign='public_id', _as='type'),
            self.unwind_({'path': '$type'}),
            self.match_({'type': {'$ne': None}}),
            self.lookup_(_from='management.users', _local='author_id', _foreign='public_id', _as='author'),
            self.unwind_({'path': '$author', 'preserveNullAndEmptyArrays': True}),
            self.lookup_(_from='management.users', _local='editor_id', _foreign='public_id', _as='editor'),
            self.unwind_({'path': '$editor', 'preserveNullAndEmptyArrays': True}),
        ]
        self.query = Pipeline(loading_dep_preset)

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for pipe in filter:
                self.query.append(pipe)

        if user and permission:
            self.query += (AccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]

        # TODO: Remove nasty quick hack
        if sort.startswith('fields'):
            sort_value = sort[7:]
            self.query.append({'$addFields': {
                'order': {
                    '$filter': {
                        'input': '$fields',
                        'as': 'fields',
                        'cond': {'$eq': ['$$fields.name', sort_value]}
                    }
                }
            }})
            self.query.append({'$sort': {'order': order}})
        else:
            self.query.append(self.sort_(sort=sort, order=order))

        self.query += results_query

        return self.query


    def count(self, filter: Union[list[dict], dict], user: UserModel = None,
              permission: AccessControlPermission = None) -> Union[Query, Pipeline]:
        """
        Count the number of documents in the stages
        Args:
            filter: filter requirement
            user: request user
            permission: acl permission

        Returns:
            Query with count stages.
        """
        self.clear()
        self.query = Pipeline([])

        if isinstance(filter, dict):
            self.query.append(self.match_(filter))
        elif isinstance(filter, list):
            for pipe in filter:
                self.query.append(pipe)

        if user and permission:
            self.query += (AccessControlQueryBuilder().build(group_id=PublicID(user.group_id), permission=permission))

        self.query.append(self.count_('total'))
        return self.query

# -------------------------------------------------------------------------------------------------------------------- #
#                                                     ObjectManager                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
class ObjectManager(ManagerBase):
    """
    Extends: ManagerBase
    """

    def __init__(self, database_manager: DatabaseManagerMongo,
                 event_queue: Union[Queue, Event] = None,
                 database: str = None):
        self.event_queue = event_queue
        self.object_builder = ObjectQueryBuilder()

        if database:
            database_manager.connector.set_database(database)

        self.objects_manager = ObjectsManager(database_manager)
        super().__init__(CmdbObject.COLLECTION, database_manager=database_manager)



# ---------------------------------------------------- CRUD - READ --------------------------------------------------- #

    def get(self, public_id: Union[PublicID, int], user: UserModel = None,
            permission: AccessControlPermission = None) -> CmdbObject:
        """
        Get a single object by its id.

        Args:
            public_id (int): ID of the object.
            user: Request user
            permission: ACL permission

        Returns:
            CmdbObject: Instance of CmdbObject with data.
        """
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)

        for resource_result in cursor_result.limit(-1):
            resource = CmdbObject.from_data(resource_result)
            type_ = self.objects_manager.get_object_type(resource.type_id)
            verify_access(type_, user, permission)
            return resource

        raise ManagerGetError(f'Object with ID: {public_id} not found!')


    def iterate(self, filter: Union[list[dict], dict], limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[CmdbObject]:
        """TODO: document"""
        try:
            query: Pipeline = self.object_builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order,
                                                        user=user, permission=permission)
            count_query: Pipeline = self.object_builder.count(filter=filter, user=user, permission=permission)
            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err

        iteration_result: IterationResult[CmdbObject] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(CmdbObject)

        return iteration_result


    def references(self, object_: CmdbObject, filter: dict, limit: int, skip: int, sort: str, order: int,
                   user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[CmdbObject]:
        """TODO: document"""
        query = []

        if isinstance(filter, dict):
            query.append(filter)
        elif isinstance(filter, list):
            query += filter

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

        # limit and skip will be handled when merged with the MDS results in '__merge_mds_references()'
        result = self.iterate(filter=query,
                              limit=0,
                              skip=0,
                              sort=sort,
                              order=order,
                              user=user,
                              permission=permission)
        mds_result = self.get_mds_references_for_object(object_, filter)

        merge_result = self.__merge_mds_references(mds_result, result, limit, skip, sort, order)

        return merge_result


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
            results = list(self._aggregate(TypeModel.COLLECTION, query))
        except ManagerIterationError as err:
            #TODO: ERROR-FIX
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

# --------------------------------------------------- CRUD - UPDATE -------------------------------------------------- #

    def update(self, public_id: Union[PublicID, int], data: Union[CmdbObject, dict], user: UserModel = None,
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

        type_ = self.objects_manager.get_object_type(instance.get('type_id'))

        if not type_.active:
            #TODO: ERROR-FIX
            raise AccessDeniedError(f'Objects cannot be updated because type `{type_.name}` is deactivated.')
        verify_access(type_, user, permission)

        update_result = self._update(self.collection, filter={'public_id': public_id}, resource=instance)

        if update_result.matched_count != 1:
            raise ManagerUpdateError('Something happened during the update!')

        if self.event_queue and user:
            event = Event("cmdb.core.object.updated", {"id": public_id, "type_id": instance.get('type_id'),
                                                       "user_id": user.get_public_id(), 'event': 'update'})
            self.event_queue.put(event)

        return update_result


    def update_many(self, query: dict, update: dict, add_to_set: bool = False):
        """
        update all documents that match the filter from a collection.
        Args:
            query (dict): A query that matches the documents to update.
            update (dict): The modifications to apply.

        Returns:
            acknowledgment of database
        """
        try:
            update_result = self._update_many(self.collection, query=query, update=update, add_to_set=add_to_set)
        except (ManagerUpdateError, AccessDeniedError) as err:
            #TODO: ERROR-FIX
            raise err

        return update_result

# --------------------------------------------------- CRUD - DELETE -------------------------------------------------- #

    def delete_all_object_references(self, public_id: int):
        """
        Delete all references to the object with the given public_id

        Args:
            public_id (int): public_id of targeted object
        """
        object_instance: CmdbObject = self.get(public_id)
        # Get all objects which reference the targeted object
        iteration_result: IterationResult = self.references(
                                                    object_=object_instance,
                                                    filter={'$match': {'active': {'$eq': True}}},
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
            self.update(refed_object_id, refed_object)

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
                LOGGER.debug("References sorting error: %s", err)

            # just keep the given limit of objects if limit > 0
            if limit > 0:
                list_length = limit + skip

                # if the list_length is longer than the object_list then just set it to len(object_list)
                if list_length > len(obj_result.results):
                    list_length = len(obj_result.results)

                try:
                    obj_result.results = obj_result.results[skip:list_length]
                except Exception as err:
                    LOGGER.debug("References list slice error: %s", err)

            # obj_result.total = len(obj_result.results)
        except Exception as err:
            LOGGER.info("[__merge_mds_references] Errorr: %s", err)

        return obj_result


    def __is_ref_field(self, field_name: str, ref_object: dict) -> bool:
        """TODO: document"""
        ref_type = self.objects_manager.get_object_type(ref_object["type_id"])
        for field in ref_type.fields:
            if field["name"] == field_name and field["type"] == "ref":
                return True

        return False
