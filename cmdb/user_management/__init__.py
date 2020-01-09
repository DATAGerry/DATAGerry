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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Basic user functions such as create, change and delete are implemented here.
In addition, the rights management, group administration and access rights are defined here.
"""
from typing import List

from cmdb.user_management.user import User
from cmdb.user_management.user_base import UserManagementBase
from cmdb.user_management.user_group import UserGroup
from cmdb.user_management.user_manager import UserManager

__COLLECTIONS__: List[object] = [
    User,
    UserGroup
]

__ADMIN_GROUP_RIGHTS__: List[str] = [
    'base.*'
]

__USER_GROUP_RIGHTS__: List[str] = [
    'base.framework.object.*',
    'base.framework.type.view',
    'base.framework.category.view',
    'base.framework.log.view',
    'base.user-management.user.view',
    'base.user-management.group.view'
]

__FIXED_GROUPS__: List[UserGroup] = [
    UserGroup(public_id=1, name='admin', label='Administrator', rights=__ADMIN_GROUP_RIGHTS__, deletable=False),
    UserGroup(public_id=2, name='user', label='User', rights=__USER_GROUP_RIGHTS__, deletable=False)
]

