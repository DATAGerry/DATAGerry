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
Basic user functions such as create, change and delete are implemented here.
In addition, the rights management, group administration and access rights are defined here.
"""
from cmdb.manager.rights_manager import RightsManager

from cmdb.user_management.models.settings import UserSettingModel
from cmdb.user_management.models.user import UserModel
from cmdb.user_management.models.right import BaseRight
from cmdb.user_management.models.group import UserGroupModel
from cmdb.user_management.rights import __all__ as rights
# -------------------------------------------------------------------------------------------------------------------- #

# TODO: Refactor to use with dependency injection

rights_manager = RightsManager(rights)

__COLLECTIONS__: list = [
    UserModel,
    UserSettingModel,
    UserGroupModel
]

__ADMIN_GROUP_RIGHTS__: list[BaseRight] = [
    rights_manager.get_right('base.*')
]

__USER_GROUP_RIGHTS__: list[BaseRight] = [
    rights_manager.get_right('base.framework.object.*'),
    rights_manager.get_right('base.framework.type.view'),
    rights_manager.get_right('base.framework.category.view'),
    rights_manager.get_right('base.framework.log.view'),
    rights_manager.get_right('base.user-management.user.view'),
    rights_manager.get_right('base.user-management.group.view'),
    rights_manager.get_right('base.docapi.template.view')
]

__FIXED_GROUPS__: list[UserGroupModel] = [
    UserGroupModel(public_id=1, name='admin', label='Administrator', rights=__ADMIN_GROUP_RIGHTS__),
    UserGroupModel(public_id=2, name='user', label='User', rights=__USER_GROUP_RIGHTS__)
]
