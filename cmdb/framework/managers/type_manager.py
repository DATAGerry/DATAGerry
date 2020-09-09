# DATAGERRY - OpenSource Enterprise CMDB
# Copyright (C) 2019 NETHINKS GmbH
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
from typing import Union

from cmdb.data_storage.database_manager import DatabaseManagerMongo
from cmdb.framework import TypeModel
from cmdb.framework.managers.framework_manager import FrameworkManager
from cmdb.framework.results.iteration import IterationResult
from cmdb.framework.utils import PublicID


class TypeManager(FrameworkManager):
    """
    Manager for the type module. Manages the CRUD functions of the types and the iteration over the collection.
    """

    def __init__(self, database_manager: DatabaseManagerMongo):
        """
        Constructor of `TypeManager`

        Args:
            database_manager: Connection to the database class.
        """
        super(TypeManager, self).__init__(TypeModel.COLLECTION, database_manager=database_manager)

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
            *args:
            **kwargs:

        Returns:
            IterationResult: Instance of IterationResult with generic TypeModel.
        """
        iteration_result: IterationResult[TypeModel] = super(TypeManager, self).iterate(
            filter=filter, limit=limit, skip=skip, sort=sort, order=order)
        iteration_result.convert_to(TypeModel)
        return iteration_result

    def get(self, public_id: Union[PublicID, int]) -> TypeModel:
        """
        Get a single type by its id.

        Args:
            public_id (int): ID of the type.

        Returns:
            TypeModel: Instance of TypeModel with data.
        """
        result = super(TypeManager, self).get(public_id=public_id)
        return TypeModel.from_data(result)

    def insert(self, type: dict) -> PublicID:
        """
        Insert a single type into the system.

        Args:
            type (dict): Raw data of the type.

        Notes:
            If no public id was given, the database manager will auto insert the next available ID.

        Returns:
            int: The Public ID of the new inserted type
        """
        return super(TypeManager, self).insert(resource=type)

    def update(self, public_id: Union[PublicID, int], type: Union[TypeModel, dict]):
        """
        Update a existing type in the system.
        Args:
            public_id (int): PublicID of the type in the system.
            type:

        Notes:
            If a TypeModel instance was passed as type argument, \
            it will be auto converted via the model `to_json` method.
        """
        if isinstance(type, TypeModel):
            type = TypeModel.to_json(type)
        return super(TypeManager, self).update(public_id=public_id, resource=type)

    def delete(self, public_id: Union[PublicID, int]) -> TypeModel:
        """
        Delete a existing type by its PublicID.

        Args:
            public_id (int): PublicID of the type in the system.

        Returns:
            TypeModel: The deleted type as its model.
        """
        type: TypeModel = self.get(public_id=public_id)
        super(TypeManager, self).delete(public_id=public_id)
        return type
