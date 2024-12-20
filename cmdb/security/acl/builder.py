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
"""TODO: document"""
from cmdb.manager.query_builder.pipeline_builder import PipelineBuilder
from cmdb.security.acl.permission import AccessControlPermission
# -------------------------------------------------------------------------------------------------------------------- #

class LookedAccessControlQueryBuilder(PipelineBuilder):
    """Query builder for looked objects in aggregation calls."""

    def __init__(self, pipeline: list[dict] = None):
        super().__init__(pipeline=pipeline)


    def build(self, group_id: int, permission: AccessControlPermission, *args, **kwargs) -> list[dict]:
        """TODO: document"""
        self.clear()
        self.add_pipe(self._lookup_types())
        self.add_pipe(self._unwind_types())
        self.add_pipe(self._match_acl(group_id, permission))
        return self.pipeline


    def _lookup_types(self) -> dict:
        return {
            '$lookup': {
                'from': 'framework.types',
                'localField': 'object.type_id',  # Field in the current collection
                'foreignField': 'public_id',     # Field in the 'framework.types' collection
                'as': 'type'
            }
        }


    def _unwind_types(self) -> dict:
        unwind = self.unwind_(path='$type')
        return unwind


    def _match_acl(self, group_id: int, permission: AccessControlPermission) -> dict:
        return self.match_(
            self.or_([
                self.exists_('type.acl', False),
                {'type.acl.activated': False},
                self.and_([
                    self.exists_(f'type.acl.groups.includes.{group_id}', True),
                    {f'type.acl.groups.includes.{group_id}': {'$all': [permission.value]}}
                ])
            ])
        )


#TODO: CLASS-FIX
class AccessControlQueryBuilder(PipelineBuilder):
    """Query builder for restrict objects in aggregation calls."""

    def __init__(self, pipeline: list[dict] = None):
        super().__init__(pipeline=pipeline)


    def build(self, group_id: int, permission: AccessControlPermission, *args, **kwargs) -> list[dict]:
        self.clear()
        self.add_pipe(self._lookup_types())
        self.add_pipe(self._unwind_types())
        self.add_pipe(self._match_acl(group_id, permission))
        return self.pipeline


    def _lookup_types(self) -> dict:
        """TODO: document"""
        return {
            '$lookup': {
                'from': 'framework.types',
                'localField': 'type_id',    # Field from the current collection
                'foreignField': 'public_id', # Field from the 'framework.types' collection
                'as': 'type'
            }
        }


    def _unwind_types(self) -> dict:
        unwind = self.unwind_(path='$type')
        return unwind


    def _match_acl(self, group_id: int, permission: AccessControlPermission) -> dict:
        return self.match_(
            self.or_([
                self.exists_('type.acl', False),
                {'type.acl.activated': False},
                self.and_([
                    self.exists_(f'type.acl.groups.includes.{group_id}', True),
                    {f'type.acl.groups.includes.{group_id}': {'$all': [permission.value]}}
                ])
            ])
        )
