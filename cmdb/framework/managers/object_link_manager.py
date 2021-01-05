# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 - 2021 NETHINKS GmbH
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
from datetime import datetime
from typing import Union, List

from cmdb.database.managers import DatabaseManagerMongo
from cmdb.framework import ObjectLinkModel
from cmdb.framework.cmdb_object_manager import CmdbObjectManager
from cmdb.framework.managers.framework_manager import FrameworkManager, FrameworkQueryBuilder
from cmdb.framework.results import IterationResult
from cmdb.framework.utils import PublicID
from cmdb.manager import ManagerGetError, ManagerIterationError, ManagerDeleteError
from cmdb.search import Query, Pipeline
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.user_management import UserModel


class ObjectLinkQueryBuilder(FrameworkQueryBuilder):

    def __init__(self):
        super(ObjectLinkQueryBuilder, self).__init__()

    def build(self, public_id: int, limit: int, skip: int, sort: str, order: int,
              user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) -> \
            Union[Query, Pipeline]:
        self.clear()
        self.query = Pipeline([])

        self.query.append(
            self.match_(
                self.or_([
                    {'primary': public_id},
                    {'secondary': public_id}
                ])
            )
        )

        if user and permission:
            pass  # TODO: ACLs

        if limit == 0:
            results_query = [self.skip_(limit)]
        else:
            results_query = [self.skip_(skip), self.limit_(limit)]
        self.query.append(self.sort_(sort=sort, order=order))

        self.query.append(self.facet_({
            'meta': [self.count_('total')],
            'results': results_query
        }))

        return self.query


class ObjectLinkManager(FrameworkManager):

    def __init__(self, database_manager: DatabaseManagerMongo):
        self.query_builder = ObjectLinkQueryBuilder()
        self.object_manager = CmdbObjectManager(database_manager)  # TODO: Replace when object api is updated
        super(ObjectLinkManager, self).__init__(ObjectLinkModel.COLLECTION, database_manager=database_manager)

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

    def iterate(self, public_id: int, limit: int, skip: int, sort: str, order: int,
                user: UserModel = None, permission: AccessControlPermission = None, *args, **kwargs) \
            -> IterationResult[ObjectLinkModel]:
        """
        Iterate over a collection where the public id exists.
        """

        try:
            query: Query = self.query_builder.build(public_id=public_id, limit=limit, skip=skip, sort=sort, order=order,
                                                    user=user, permission=permission)
            aggregation_result = next(self._aggregate(self.collection, query))
        except ManagerGetError as err:
            raise ManagerIterationError(err=err)
        iteration_result: IterationResult[ObjectLinkModel] = IterationResult.from_aggregation(aggregation_result)
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
            link['creation_time'] = datetime.now()
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
