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
from datetime import datetime

import pytest

from cmdb.user_management import UserGroupModel, RightManager, UserModel
# -------------------------------------------------------------------------------------------------------------------- #

@pytest.fixture(scope="session")
def right_manager():
    """TODO: document"""
    from cmdb.user_management import rights
    return RightManager(rights)


@pytest.fixture(scope="session")
def full_access_group(right_manager: RightManager):
    "TODO: document"
    return UserGroupModel(public_id=1, name='full', label='Full', rights=[right_manager.get('base.*')])


@pytest.fixture(scope="session")
def none_access_group():
    """TODO: document"""
    return UserGroupModel(public_id=2, name='none', label='None')


@pytest.fixture(scope="session")
def full_access_user(full_access_group: UserGroupModel):
    "TODO: document"
    registration_time = datetime.now()
    return UserModel(public_id=1, user_name='full-access-user',
                     active=True, group_id=full_access_group.public_id,
                     registration_time=registration_time)


@pytest.fixture(scope="session")
def none_access_user(none_access_group: UserGroupModel):
    "TODO: document"
    registration_time = datetime.now()
    return UserModel(public_id=2, user_name='none-access-user',
                     active=True, group_id=none_access_group.public_id,
                     registration_time=registration_time)
