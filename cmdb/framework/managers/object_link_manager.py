# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2023 becon GmbH
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
"""TODO: document"""
from datetime import datetime, timezone
from typing import Union, List

from cmdb.database.database_manager_mongo import DatabaseManagerMongo
from cmdb.framework import ObjectLinkModel
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.manager.managers import ManagerBase
from cmdb.framework.managers.object_manager import ObjectQueryBuilder
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerDeleteError
from cmdb.search import Pipeline
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel
# -------------------------------------------------------------------------------------------------------------------- #

class ObjectLinkManager(ManagerBase):
    """TODO: document"""

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.query_builder = ObjectQueryBuilder()
        self.object_manager = CmdbObjectManager(database_manager)  # TODO: Replace when object api is updated
        super().__init__(ObjectLinkModel.COLLECTION, database_manager=database_manager)


    def get(self, public_id: Union[PublicID, int], user: UserModel = None,
            permission: AccessControlPermission = None) -> ObjectLinkModel:
        """
        Get a single link by its id.

        Args:
            public_id (int): ID of the link.
            user: request user
            permission: acl permission

        Returns:
            ObjectLinkModel: Instance of CmdbLink with data.
        """
        cursor_result = self._get(self.collection, filter={'public_id': public_id}, limit=1)
        for resource_result in cursor_result.limit(-1):
            link = ObjectLinkModel.from_data(resource_result)
            if user and permission:
                self.object_manager.get_object(public_id=link.primary, user=user, permission=permission)
                self.object_manager.get_object(public_id=link.secondary, user=user, permission=permission)
            return link
        raise ManagerGetError(f'ObjectLinkModel with ID: {public_id} not found!')


    def iterate(self, filter: Union[List[dict], dict], limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[ObjectLinkModel]:
        """
        Iterate over a collection where the public id exists.
        """

        try:
            query: Pipeline = self.query_builder.build(filter=filter, limit=limit, skip=skip, sort=sort, order=order)

            #Links don't have a type_id
            #TODO: integrate quick fix in basic workflow (DAT-348)
            query[1]['$unwind'] = {"path": "$type", "preserveNullAndEmptyArrays": True}
            del query[2]

            count_query: Pipeline = self.query_builder.count(filter=filter, user=user, permission=permission)

            #Links don't have a type_id
            #TODO: integrate quick fix in basic workflow (DAT-348)
            del count_query[2]

            aggregation_result = list(self._aggregate(self.collection, query))
            total_cursor = self._aggregate(self.collection, count_query)
            total = 0
            while total_cursor.alive:
                total = next(total_cursor)['total']
        except ManagerGetError as err:
            raise ManagerIterationError(err) from err
        iteration_result: IterationResult[ObjectLinkModel] = IterationResult(aggregation_result, total)
        iteration_result.convert_to(ObjectLinkModel)
        return iteration_result


    def insert(self, link: Union[dict, ObjectLinkModel], user: UserModel = None,
               permission: AccessControlPermission = AccessControlPermission.CREATE) -> PublicID:
        """
        Insert a single link into the system.

        Args:
            link (ObjectLinkModel): Raw data of the link.
            user: request user
            permission: acl permission

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted link
        """
        if isinstance(link, ObjectLinkModel):
            link = ObjectLinkModel.to_json(link)
        if 'creation_time' not in link:
            link['creation_time'] = datetime.now(timezone.utc)
        if user and permission:
            self.object_manager.get_object(public_id=link['primary'], user=user, permission=permission)
            self.object_manager.get_object(public_id=link['secondary'], user=user, permission=permission)

        return self._insert(self.collection, resource=link)


    def update(self, public_id: PublicID, link: Union[ObjectLinkModel, dict]):
        raise NotImplementedError


    def delete(self, public_id: PublicID, user: UserModel = None,
               permission: AccessControlPermission = AccessControlPermission.DELETE) -> ObjectLinkModel:
        """
        Delete a existing link by its PublicID.

        Args:
            public_id (int): PublicID of the link in the system.
            user: request user
            permission: acl permission

        Returns:
            ObjectLinkModel: The deleted link as its model.
        """
        link: ObjectLinkModel = self.get(public_id=public_id)
        if user and permission:
            self.object_manager.get_object(public_id=link.primary, user=user, permission=permission)
            self.object_manager.get_object(public_id=link.secondary, user=user, permission=permission)
        delete_result = self._delete(self.collection, filter={'public_id': public_id})

        if delete_result.deleted_count == 0:
            raise ManagerDeleteError(err='No link matched this public id')
        return link
