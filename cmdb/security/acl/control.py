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
from cmdb.security.acl.permission import AccessControlPermission
from cmdb.security.acl.sections import GroupACL, T
# -------------------------------------------------------------------------------------------------------------------- #

class AccessControlList:
    """
    The actual implementation of the Access Control List (ACL).
    """

    def __init__(self, activated: bool, groups: GroupACL = None):
        self.activated = activated
        self.groups: GroupACL = groups

    @classmethod
    def from_data(cls, data: dict) -> "AccessControlList":
        """TODO: document"""
        return cls(
            activated=data.get('activated', False),
            groups=GroupACL.from_data(data.get('groups', {}))
        )

    @classmethod
    def to_json(cls, acl: "AccessControlList") -> dict:
        """TODO: document"""
        return {
            'activated': acl.activated,
            'groups': GroupACL.to_json(acl.groups)
        }

    def grant_access(self, key: T, permission: AccessControlPermission, section: str = None):
        """TODO: document"""
        if section == 'groups':
            self.groups.grant_access(key, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def revoke_access(self, key: T, permission: AccessControlPermission, section: str = None):
        """TODO: document"""
        if section == 'groups':
            self.groups.grant_access(key, permission)
        else:
            raise ValueError(f'No ACL section with name: {section}')

    def verify_access(self, key: T, permission: AccessControlPermission) -> bool:
        """TODO: document"""
        return self.groups.verify_access(key, permission)
