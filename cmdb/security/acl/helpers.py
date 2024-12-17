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
"""Access Control helper functions"""
import logging

from cmdb.security.acl.control import AccessControlList
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.models.type_model.type import TypeModel
from cmdb.models.user_model.user import UserModel

from cmdb.errors.security import AccessDeniedError
# -------------------------------------------------------------------------------------------------------------------- #

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #

def has_access_control(model: TypeModel, user: UserModel, permission: AccessControlPermission) -> bool:
    """Check if a user has access to object/objects for a given permission"""
    acl: AccessControlList = model.acl

    if acl and acl.activated:
        return acl.verify_access(user.group_id, permission)

    return True


def verify_access(model: TypeModel, user: UserModel = None, permission: AccessControlPermission = None):
    """Validate if a user has access to objects of this type."""
    if not user or not permission:
        return

    verify = has_access_control(model, user, permission)

    if not verify:
        #TODO: ERROR-FIX
        raise AccessDeniedError('Protected by ACL permission!')
